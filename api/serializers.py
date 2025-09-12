from rest_framework.serializers import (CharField, HyperlinkedModelSerializer,
                                        HyperlinkedRelatedField,
                                        PrimaryKeyRelatedField)

from .models import Event, Package


class PackageSerializer(HyperlinkedModelSerializer):
    identifier = CharField()

    class Meta:
        model = Package
        fields = '__all__'
        datatables_always_serialize = ('identifier',)


class PackageListSerializer(HyperlinkedModelSerializer):
    error_identifier = PrimaryKeyRelatedField(
        queryset=Event.objects.all(),
        many=False)
    error_message = CharField(source='error_identifier.message', read_only=True)

    class Meta:
        model = Package
        fields = ['url', 'identifier', 'origin', 'title', 'status', 'created', 'error_identifier', 'error_message']
        datatables_always_serialize = ('error_identifier',)


class EventSerializer(HyperlinkedModelSerializer):
    identifier = CharField()
    package_identifier = PrimaryKeyRelatedField(
        queryset=Package.objects.all(),
        many=False)
    package_origin = CharField(source='package_identifier.origin', read_only=True)
    package_title = CharField(source='package_identifier.title', read_only=True)
    package_url = HyperlinkedRelatedField(
        source='package_identifier',
        view_name='package-detail',
        many=False,
        read_only=True
    )

    class Meta:
        model = Event
        fields = '__all__'
        datatables_always_serialize = ('identifier',)
