from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Event, Package
from .serializers import EventSerializer, PackageSerializer


class PackageViewSet(ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

    @action(detail=True)
    def events(self, request, pk=None):
        package = get_object_or_404(Package, pk=pk)
        serializer = EventSerializer(package.event_set.all, many=True)
        return Response(serializer.data)


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
