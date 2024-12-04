from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreditViewSet,  get_encours_credits_for_admins, get_users_with_ongoing_credits

router = DefaultRouter()
router.register(r'credits', CreditViewSet, basename='credit')

urlpatterns = [
    path('', include(router.urls)),
    path('credits/encours/admins/', get_encours_credits_for_admins, name='encours-credits-admins'),
    path('admin/ongoing-credits/', get_users_with_ongoing_credits, name='admin-ongoing-credits'),



]
