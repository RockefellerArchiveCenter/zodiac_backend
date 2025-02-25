from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Event, Package


class PackageSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Package
        fields = ['__all__']


class EventSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ['__all__']
