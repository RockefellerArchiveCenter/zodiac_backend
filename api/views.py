from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .clients import AWSClient
from .models import Event, Package
from .serializers import (EventSerializer, PackageListSerializer,
                          PackageSerializer)


class PackageViewSet(ModelViewSet):
    """Handles Package data."""
    queryset = Package.objects.all().order_by('-created')
    serializer_class = PackageSerializer
    filterset_fields = ['origin']

    def get_serializer_class(self):
        if self.action == "list":
            return PackageListSerializer
        return PackageSerializer

    def partial_update(self, request, pk=None):
        """Merge identifiers."""
        instance = self.get_object()
        request.data.get('identifiers', {}).update(instance.identifiers)
        return super().partial_update(request, pk)

    @action(detail=True)
    def events(self, request, pk=None):
        """Show events related to a package."""
        package = get_object_or_404(Package, pk=pk)
        serializer = EventSerializer(
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

    def post(self, request, **kwargs):
        try:
            service = request.POST['service']
            package_id = request.POST['package_id']
        except KeyError:
            return Response("Post data must include both service and package_id.", status=500)

        try:
            client = AWSClient()
            output = client.publish_restart_message(package_id, service)
            return Response(output)
        except Exception as e:
            return Response(f"Error sending restart message: {e}", status=500)
