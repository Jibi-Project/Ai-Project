
from django.contrib import admin
from django.db import router
from django.urls import path, include
from api.views import CreateUserView, LoginView, LogoutView, change_password, forgot_password ,profile, reset_password
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from ml_integration.views import get_loan_prediction_by_id, predict_loan_status, add_loan_prediction

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
    path('ml_integration/predict-loan-status/', predict_loan_status, name='predict-loan-status'),
    path('ml_integration/predict-loan-status/add', add_loan_prediction, name='predict-loan-status'),
    path('ml_integration/predict-loan-status/<int:loan_id>/', predict_loan_status, name='get_loan_by_id'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    
    path('loan_prediction/<int:loan_prediction_id>/', get_loan_prediction_by_id, name='get_loan_prediction_by_id'),


]



