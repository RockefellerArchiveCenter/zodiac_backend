import boto3
from aws_assume_role_lib import assume_role
from django.conf import settings


class AWSClient(object):

    def __init__(self):
        session = boto3.Session()
        assumed_role_session = assume_role(
            session,
            settings.AWS_ROLE_ARN,
            region_name=settings.AWS_REGION)
        self.client = assumed_role_session.client('sns')
        self.topic_arn = settings.AWS_SNS_TOPIC_ARN

    def publish_restart_message(self, package_id, service):
        self.client.publish(
            TopicArn=self.topic_arn,
            Message=f'Start service {service} for package {package_id}',
            MessageAttributes={
                'package_id': {
                    'DataType': 'String',
                    'StringValue': package_id,
                },
                'requested_status': {
                    'DataType': 'String',
                    'StringValue': 'START'
                },
                'service': {
                    'DataType': 'String',
                    'StringValue': service,
                }
            })
        return f"Service {service} started successfully."
