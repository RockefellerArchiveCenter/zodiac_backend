import boto3
from aws_assume_role_lib import assume_role
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Event, Package
from .serializers import (EventSerializer, PackageEventSerializer,
                          PackageListSerializer, PackageSerializer)


class PackageViewSet(ModelViewSet):
    """Handles Package data."""
    queryset = Package.objects.all().order_by('-created')
    serializer_class = PackageSerializer
    filterset_fields = ['origin']

    def get_serializer_class(self):
        if self.action == "list":
            return PackageListSerializer
        return PackageSerializer

    @action(detail=True)
    def events(self, request, pk=None):
        """Show events related to a package."""
        package = get_object_or_404(Package, pk=pk)
        serializer = PackageEventSerializer(
            package.event_set.all().order_by('-created'),
            context={'request': request},
            many=True)
        return Response(serializer.data)


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all().order_by('-created')
    serializer_class = EventSerializer
    filterset_fields = ['outcome', 'service']


class RestartServiceView(APIView):
    """Allows users to restart failed services."""

    def create(self, request, **kwargs):
        try:
            service = request.POST['service']
            package_id = request.POST['package_id']
        except KeyError as e:
            raise Exception(f"Post data must include both service and package_id, missing {str(e)}.")

        session = boto3.Session()
        assumed_role_session = assume_role(
            session,
            settings.AWS_ROLE_ARN,
            region_name=settings.AWS_REGION)
        client = assumed_role_session.client('sns')
        client.publish(
            TopicArn=settings.AWS_SNS_TOPIC_ARN,
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
        return Response(f"Service {service} started successfully.")
