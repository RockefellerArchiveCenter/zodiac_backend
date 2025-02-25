from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Event, Package
from .serializers import (EventSerializer, PackageEventSerializer,
                          PackageListSerializer, PackageSerializer)


class PackageViewSet(ModelViewSet):
    queryset = Package.objects.all().order_by('-created')
    serializer_class = PackageSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PackageListSerializer
        return PackageSerializer

    @action(detail=True)
    def events(self, request, pk=None):
        """Show events related to a package."""
        package = get_object_or_404(Package, pk=pk)
        serializer = PackageEventSerializer(package.event_set.all().order_by('created'), many=True)
        return Response(serializer.data)


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all().order_by('-created')
    serializer_class = EventSerializer
