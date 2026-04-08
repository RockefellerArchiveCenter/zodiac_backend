import json

from django.test import TestCase
from django.urls import reverse

from .models import Event, Package


class SignalTests(TestCase):

    def test_update_status(self):
        """Asserts status and error message fields are correctly updated when error message is added."""
        package = Package.objects.create(
            identifier="f78742e5-6af9-4756-a94a-6cd297406d51",
            origin="aurora",
            title="Organizational Charts")
        self.assertEqual(package.status, 'IN PROCESS')

        error = Event.objects.create(
            identifier="f78742e5-6af9-4756-a94a-6cd297406d55",
            outcome="FAILURE",
            service="digital_ingest_discovery",
            package_identifier=package,
            message="Could not find file /tmp/f78742e5-6af9-4756-a94a-6cd297406d55 \n  in transform.py line 23",
        )
        package.refresh_from_db()
        self.assertEqual(package.status, "ERROR")
        self.assertEqual(package.error_message, "Could not find file /tmp/f78742e5-6af9-4756-a94a-6cd297406d55 \n  in transform.py line 23")

        in_process = Event.objects.create(
            identifier="f78742e5-6af9-4756-a94a-6cd297406d56",
            outcome="COMPLETE",
            service="digital_ingest_discovery",
            package_identifier=package,
            message="Discovery complete",
        )
        package.refresh_from_db()
        self.assertEqual(package.status, "IN PROCESS")

        complete = Event.objects.create(
            identifier="f78742e5-6af9-4756-a94a-6cd297406d57",
            outcome="SUCCESS",
            service="digital_ingest_transformation",
            package_identifier=package,
            message="Transformation complete",
        )
        package.refresh_from_db()
        self.assertEqual(package.status, "COMPLETE")
        self.assertIsNone(package.error_message)

        complete.delete()
        package.refresh_from_db()
        self.assertEqual(package.status, "IN PROCESS")
        self.assertIsNone(package.error_message)

        in_process.delete()
        package.refresh_from_db()
        self.assertEqual(package.status, "ERROR")
        self.assertEqual(package.error_message, "Could not find file /tmp/f78742e5-6af9-4756-a94a-6cd297406d55 \n  in transform.py line 23")

        error.delete()
        package.refresh_from_db()
        self.assertEqual(package.status, "IN PROCESS")
        self.assertIsNone(package.error_message)


class ViewTests(TestCase):
    fixtures = ['api/fixtures/initial.json']

    def test_events_action(self):
        """Asserts events action produces expected data."""
        for package_id, expected_events in [
                ("f78742e5-6af9-4756-a94a-6cd297406d51", 3),
                ("8bf992c0-1547-403a-93d4-ac531e7ed080", 0)]:
            response = self.client.get(reverse('package-events', kwargs={"pk": package_id}))
            self.assertEqual(len(response.data), expected_events)

    def test_find_by_id_action(self):
        """Asserts find by ID endpoint returns expected packages."""
        for params, expected_packages in [
                ("archivematica_uuid=0a9c6171-a18d-4ff6-b9e7-bef01aaded11", 0),
                ("archivematica_uuid=0a9c6171-a18d-4ff6-b9e7-bef01aaded10", 2),
                ("archivesspace_archival_object=/repositories/2/archival_objects/2153", 1),
                ("archivesspace_digital_objects=/repositories/2/digital_objects/3", 1),
                ("archivesspace_archival_object=/repositories/2/archival_objects/2153&archivematica_uuid=0a9c6171-a18d-4ff6-b9e7-bef01aaded10", 1)]:
            response = self.client.get(f"{reverse('package-find-by-id')}?{params}")
            self.assertEqual(len(response.data), expected_packages)

    def test_partial_update(self):
        package_id = "8bf992c0-1547-403a-93d4-ac531e7ed080"
        initial_package = Package.objects.get(identifier=package_id)
        initial_identifiers = initial_package.identifiers

        # Test adding new identifier
        output = self.client.patch(
            reverse('package-detail', kwargs={"pk": package_id}),
            data=json.dumps({"identifiers": {"new_id": "bar"}}),
            headers={"Content-Type": "application/json"}
        ).json()

        self.assertEqual(len(initial_identifiers.keys()) + 1, len(output['identifiers'].keys()))
        for k, v in initial_identifiers.items():
            self.assertEqual(output['identifiers'][k], v)

        # Test updating existing identifier
        output = self.client.patch(
            reverse('package-detail', kwargs={"pk": package_id}),
            data=json.dumps({"identifiers": {"new_id": "baz"}}),
            headers={"Content-Type": "application/json"}
        ).json()

        self.assertEqual(output['identifiers']['new_id'], 'baz')

        # Test when identifiers value is None.
        self.client.patch(
            reverse('package-detail', kwargs={"pk": package_id}),
            data=json.dumps({"identifiers": None}),
            headers={"Content-Type": "application/json"}
        ).json()
