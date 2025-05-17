from django.urls import path
from .views import (
    UserRegistrationView, UserMetadataUpdateView, DocumentUploadView,
    OTPRequestView, OTPVerifyView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('update-metadata/<str:username>/', UserMetadataUpdateView.as_view(), name='user-metadata-update'),
    path('upload-documents/<str:username>/', DocumentUploadView.as_view(), name='user-document-upload'),
    path('request-otp/', OTPRequestView.as_view(), name='request-otp'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
] 