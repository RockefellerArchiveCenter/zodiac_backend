import json
from unittest.mock import patch

import boto3
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from moto import mock_aws
from moto.core import DEFAULT_ACCOUNT_ID

from .clients import AWSClient
from .models import Package
from .serializers import PackageListSerializer


class SerializerTests(TestCase):
    fixtures = ['api/fixtures/initial.json']

    def test_last_outcome(self):
        serializer = PackageListSerializer()

        for package_id, expected in [
                ("f78742e5-6af9-4756-a94a-6cd297406d51", "FAILURE"),
                ("8bf992c0-1547-403a-93d4-ac531e7ed080", None)]:
            package = Package.objects.get(pk=package_id)
            last_outcome = serializer.get_last_outcome(package)
            self.assertEqual(last_outcome, expected,)


class ViewTests(TestCase):
    fixtures = ['api/fixtures/initial.json']

    def test_events_action(self):
        """Asserts events action produces expected data."""
        for package_id, expected_events in [
                ("f78742e5-6af9-4756-a94a-6cd297406d51", 3),
                ("8bf992c0-1547-403a-93d4-ac531e7ed080", 0)]:
            response = self.client.get(reverse('package-events', kwargs={"pk": package_id}))
            self.assertEqual(len(response.data), expected_events)

    def test_restart_service_view_missing_data(self, ):
        """Asserts check for required data."""
        output = self.client.post(reverse('restart-service'))
        self.assertEqual(output.status_code, 500)
        self.assertEqual(output.data, "Post data must include both service and package_id.")

    @patch('api.clients.AWSClient.__init__')
    @patch('api.clients.AWSClient.publish_restart_message')
    def test_restart_service_view(self, mock_restart, mock_init):
        """Asserts expected methods are triggered."""
        mock_init.return_value = None
        package_id = "f78742e5-6af9-4756-a94a-6cd297406d51"
        service = "ursa_major"
        restart_message = "Service ursa_major started successfully."
        mock_restart.return_value = restart_message
        output = self.client.post(reverse('restart-service'), data={"package_id": package_id, "service": service})
        self.assertEqual(output.status_code, 200)
        self.assertEqual(output.data, restart_message)
        mock_init.assert_called_once()
        mock_restart.assert_called_once_with(package_id, service)

    @patch('api.clients.AWSClient.__init__')
    @patch('api.clients.AWSClient.publish_restart_message')
    def test_restart_service_view_handle_exception(self, mock_restart, mock_init):
        """Asserts handling of error in publish"""
        mock_init.return_value = None
        mock_restart.side_effect = Exception("error")
        output = self.client.post(reverse('restart-service'), data={"package_id": "foo", "service": "bar"})
        self.assertEqual(output.status_code, 500)
        self.assertEqual(output.data, "Error sending restart message: error")

    def test_partial_update(self):
        package_id = "8bf992c0-1547-403a-93d4-ac531e7ed080"
        initial_package = Package.objects.get(identifier=package_id)
        initial_identifiers = initial_package.identifiers

        output = self.client.patch(
            reverse('package-detail', kwargs={"pk": package_id}),
            data=json.dumps({"identifiers": {"new_id": "bar"}}),
            headers={"Content-Type": "application/json"}
        ).json()

        self.assertEqual(len(initial_identifiers.keys()) + 1, len(output['identifiers'].keys()))
        for k, v in initial_identifiers.items():
            self.assertEqual(output['identifiers'][k], v)

        output = self.client.patch(
            reverse('package-detail', kwargs={"pk": package_id}),
            data=json.dumps({"identifiers": {"new_id": "baz"}}),
            headers={"Content-Type": "application/json"}
        ).json()

        self.assertEqual(output['identifiers']['new_id'], 'baz')


class AWSClientTests(TestCase):

    @mock_aws
    @patch('api.clients.AWSClient.__init__')
    def test_publish_restart_message(self, mock_init):
        """Assert messages are published as expected."""
        mock_init.return_value = None
        service = "ursa_major"
        package_id = "12345"
        sns = boto3.client('sns', region_name=settings.AWS_REGION)
        queue_name = "test-queue"
        sns_topic_name = 'digital_ingest_topic'
        topic_arn = sns.create_topic(Name=sns_topic_name)['TopicArn']
        sqs_conn = boto3.resource("sqs", region_name=settings.AWS_REGION)
        sqs_conn.create_queue(QueueName=queue_name)
        sns.subscribe(
            TopicArn=topic_arn,
            Protocol="sqs",
            Endpoint=f"arn:aws:sqs:{settings.AWS_REGION}:{DEFAULT_ACCOUNT_ID}:{queue_name}",)

        client = AWSClient()
        client.client = boto3.client('sns', region_name=settings.AWS_REGION)
        client.topic_arn = topic_arn
        output = client.publish_restart_message(package_id, service)
        self.assertEqual(output, f'Service {service} started successfully.')

        queue = sqs_conn.get_queue_by_name(QueueName=queue_name)
        messages = queue.receive_messages(MaxNumberOfMessages=10)
        self.assertEqual(len(messages), 1)
        message_content = json.loads(messages[0].body)
        self.assertEqual(message_content['Message'], f'Start service {service} for package {package_id}')
        self.assertEqual(message_content['MessageAttributes'], {
            'package_id': {
                'Type': 'String',
                'Value': package_id},
            'requested_status': {
                'Type': 'String',
                'Value': 'START'},
            'service': {
                'Type': 'String',
                'Value': service}})
