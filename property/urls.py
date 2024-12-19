from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, PropertyTransferViewSet

router = DefaultRouter()

router.register(r"properties", PropertyViewSet, basename="property")
router.register(
    r"property-transfers", PropertyTransferViewSet, basename="property-transfer"
)

urlpatterns = [
    path("", include(router.urls)),
]
