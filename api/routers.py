from rest_framework.routers import DefaultRouter

from .views import EventViewSet, PackageViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'packages', PackageViewSet)
