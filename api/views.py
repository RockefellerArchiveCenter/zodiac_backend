from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Event, Package
from .serializers import (EventSerializer, PackageListSerializer,
                          PackageSerializer)


class PackageViewSet(ModelViewSet):
    """Handles Package data."""
    queryset = Package.objects.all().order_by('-created')
    serializer_class = PackageSerializer
    filterset_fields = ['origin', 'status']

    def get_serializer_class(self):
        if self.action == "list":
            return PackageListSerializer
        return PackageSerializer

    def partial_update(self, request, pk=None):
        """Merge identifiers."""
        instance = self.get_object()
        identifiers = instance.identifiers if instance.identifiers else {}
        request_identifiers = request.data.get('identifiers') if request.data.get('identifiers') else {}
        identifiers.update(request_identifiers)
        request.data['identifiers'] = identifiers
        return super().partial_update(request, pk)

    @action(detail=True)
    def events(self, request, pk=None):
        """Show events related to a package."""
        self.filterset_fields = ['service', 'outcome', 'message']  # set custom filter fields
        package = get_object_or_404(Package, pk=pk)
        queryset = package.event_set.all().order_by('-created')
        queryset = self.filter_queryset(queryset)  # filter queryset to apply datatables search and sort
        queryset = self.paginate_queryset(queryset)  # paginage queryset
        serializer = EventSerializer(
            queryset,
            context={'request': request},
            many=True)
        return Response(serializer.data)

    @action(detail=False)
    def find_by_id(self, request):
        request_params = dict(request.GET)
        final_params = {}
        for key, value in request_params.items():
            for v in value:
                if key == 'archivesspace_digital_objects':
                    final_params[key] = [v]
                else:
                    final_params[key] = v
        queryset = Package.objects.filter(identifiers__contains=final_params)
        serializer = PackageListSerializer(
            queryset,
            context={'request': request},
            many=True)
        return Response(serializer.data)


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all().order_by('-created')
    serializer_class = EventSerializer
    filterset_fields = ['outcome', 'service']
