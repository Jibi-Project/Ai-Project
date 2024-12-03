from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreditViewSet

router = DefaultRouter()
router.register(r'ml_integration', CreditViewSet, basename='ml_integration')

urlpatterns = [
    path('', include(router.urls)),
]
