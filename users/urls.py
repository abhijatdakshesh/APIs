from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView, UserMetadataUpdateView, DocumentUploadView,
    OTPRequestView, OTPVerifyView,
    TaskViewSet, UserTasksView, TaskSubmissionView, TaskboardView, TaskCalendarView
)

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('update-metadata/<str:username>/', UserMetadataUpdateView.as_view(), name='user-metadata-update'),
    path('upload-documents/<str:username>/', DocumentUploadView.as_view(), name='user-document-upload'),
    path('request-otp/', OTPRequestView.as_view(), name='request-otp'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
    # Task-related endpoints
    path('user/<str:username>/', UserTasksView.as_view(), name='user-tasks'),
    path('submit/', TaskSubmissionView.as_view(), name='task-submission'),
    path('taskboard/', TaskboardView.as_view(), name='taskboard'),
    path('calendar/', TaskCalendarView.as_view(), name='calendar'),
] 