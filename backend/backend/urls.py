
from django.contrib import admin
from django.db import router
from django.urls import path, include
from api.views import CreateUserView, LoginView, change_password, forgot_password ,profile, reset_password
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/user/register/", CreateUserView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path('api/login/', LoginView.as_view(), name='login'),  # Endpoint de connexion JWT
    path('api/profile/', profile, name='profile'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("api.urls")),
    path('api/', include('credit.urls')),
    path('api/change-password/', change_password, name='change_password'),
    path('api/forgot-password/', forgot_password, name='forgot_password'),
    path('api/reset-password/<int:user_id>/<str:token>/', reset_password, name='reset_password'),
]



