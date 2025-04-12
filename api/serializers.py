from rest_framework.serializers import (CharField, HyperlinkedModelSerializer,
                                        HyperlinkedRelatedField,
                                        PrimaryKeyRelatedField,
                                        SerializerMethodField)

from .models import Event, Package


class PackageSerializer(HyperlinkedModelSerializer):
    identifier = CharField()

    class Meta:
        model = Package
        fields = '__all__'


class PackageListSerializer(HyperlinkedModelSerializer):
    last_outcome = SerializerMethodField()

    class Meta:
        model = Package
        fields = ['url', 'identifier', 'origin', 'title', 'last_outcome']

    def get_last_outcome(self, obj):
        package_events = obj.event_set.all()
        if len(package_events):
            return package_events.order_by('-last_modified')[0].outcome
        return None


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
