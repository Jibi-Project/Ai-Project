from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreditViewSet

router = DefaultRouter()
router.register(r'credits', CreditViewSet, basename='credit')

urlpatterns = [
    path('', include(router.urls)),
]
