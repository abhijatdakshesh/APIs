from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from .serializers import (
    UserRegistrationSerializer, MetadataSerializer, DocumentUploadSerializer,
    OTPRequestSerializer, OTPVerifySerializer
)
from .models import UserTable
import logging

# Set up logger
logger = logging.getLogger(__name__)

# Create your views here.

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "type": user.type,
                    "email": user.email,
                    "metadata": {
                        "field_recovery_experience_years": user.field_recovery_experience_years,
                        "specialization_areas": user.specialization_areas,
                        "languages_known": user.languages_known
                    }
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserMetadataUpdateView(generics.UpdateAPIView):
    serializer_class = MetadataSerializer
    
    def get_object(self):
        username = self.kwargs.get('username')
        try:
            return UserTable.objects.get(username=username)
        except UserTable.DoesNotExist:
            raise NotFound(f"User with username {username} not found")
    
    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Update only the metadata fields
            user.field_recovery_experience_years = serializer.validated_data.get('field_recovery_experience_years')
            user.specialization_areas = serializer.validated_data.get('specialization_areas')
            user.languages_known = serializer.validated_data.get('languages_known')
            user.save()
            
            return Response({
                "message": "User metadata updated successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "type": user.type,
                    "email": user.email,
                    "metadata": {
                        "field_recovery_experience_years": user.field_recovery_experience_years,
                        "specialization_areas": user.specialization_areas,
                        "languages_known": user.languages_known
                    }
                }
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentUploadView(generics.GenericAPIView):
    serializer_class = DocumentUploadSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def get_object(self):
        username = self.kwargs.get('username')
        try:
            return UserTable.objects.get(username=username)
        except UserTable.DoesNotExist:
            raise NotFound(f"User with username {username} not found")
    
    def post(self, request, *args, **kwargs):
        user = self.get_object()
        
        # Log request information
        logger.info(f"Document upload request for user {user.username}")
        logger.info(f"Request data: {request.data}")
        logger.info(f"Files: {request.FILES}")
        
        try:
            # Process each file individually to avoid issues
            if 'aadhaar_file' in request.FILES:
                user.aadhaar_file = request.FILES['aadhaar_file']
            
            if 'pan_file' in request.FILES:
                user.pan_file = request.FILES['pan_file']
                
            if 'police_verification' in request.FILES:
                user.police_verification = request.FILES['police_verification']
                
            if 'empanelment_letter' in request.FILES:
                user.empanelment_letter = request.FILES['empanelment_letter']
            
            # Save the user object with the uploaded files
            user.save()
            
            # Prepare response with file URLs
            document_urls = {}
            for field in ['aadhaar_file', 'pan_file', 'police_verification', 'empanelment_letter']:
                file = getattr(user, field, None)
                if file and file.name:
                    document_urls[field] = request.build_absolute_uri(file.url)
            
            return Response({
                "message": "Documents uploaded successfully",
                "username": user.username,
                "documents": document_urls
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error uploading documents: {str(e)}")
            raise ParseError(f"Error uploading documents: {str(e)}")
            
        return Response({"error": "No files were uploaded"}, status=status.HTTP_400_BAD_REQUEST)


class OTPRequestView(APIView):
    """
    API endpoint for requesting an OTP using phone number
    """
    serializer_class = OTPRequestSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            
            try:
                user = UserTable.objects.get(phone_number=phone_number)
                otp = user.generate_otp()
                
                # In a real-world scenario, you would send this OTP via SMS
                # For this example, we'll just return it in the response
                return Response({
                    "message": "OTP sent successfully",
                    "phone_number": phone_number,
                    "otp": otp  # In production, remove this line and send OTP via SMS
                })
            except UserTable.DoesNotExist:
                return Response(
                    {"error": "No user found with this phone number"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerifyView(APIView):
    """
    API endpoint for verifying OTP and logging in
    """
    serializer_class = OTPVerifySerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            otp = serializer.validated_data['otp']
            
            try:
                user = UserTable.objects.get(phone_number=phone_number)
                if user.verify_otp(otp):
                    # OTP verified successfully, return user details
                    return Response({
                        "message": "OTP verified successfully",
                        "user": {
                            "id": user.id,
                            "username": user.username,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "type": user.type,
                            "phone_number": user.phone_number,
                            "email": user.email,
                            "is_verified": user.is_verified
                        }
                    })
                else:
                    return Response(
                        {"error": "Invalid or expired OTP"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except UserTable.DoesNotExist:
                return Response(
                    {"error": "No user found with this phone number"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Task Management Views (moved from tasks app)
from rest_framework import viewsets, generics, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .models import Task, TaskSubmission, TaskDocument, UserTable
from .serializers import TaskSerializer, TaskSubmissionSerializer, TaskDocumentSerializer, TaskCalendarSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'tags']
    ordering_fields = ['due_date', 'priority', 'created_date', 'status']
    ordering = ['due_date']
    def get_queryset(self):
        queryset = Task.objects.all()
        assignee_id = self.request.query_params.get('assignee')
        status = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        due_category = self.request.query_params.get('due_category')
        if assignee_id:
            queryset = queryset.filter(assignee_id=assignee_id)
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if due_category:
            now = timezone.now()
            today_end = now.replace(hour=23, minute=59, second=59)
            week_end = now + timedelta(days=(6 - now.weekday()))
            week_end = week_end.replace(hour=23, minute=59, second=59)
            if due_category == 'due_today':
                queryset = queryset.filter(due_date__lte=today_end)
            elif due_category == 'due_this_week':
                queryset = queryset.filter(due_date__gt=today_end, due_date__lte=week_end)
            elif due_category == 'upcoming':
                queryset = queryset.filter(due_date__gt=week_end)
        return queryset

class UserTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(UserTable, username=username)
        return Task.objects.filter(assignee=user).order_by('due_date')

class TaskSubmissionView(generics.CreateAPIView):
    serializer_class = TaskSubmissionSerializer
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request, *args, **kwargs):
        task_id = request.data.get('task')
        try:
            task = Task.objects.get(id=task_id)
            if task.status == 'completed':
                return Response({"error": "This task has already been completed"}, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        return super().post(request, *args, **kwargs)

class TaskboardView(APIView):
    def get(self, request):
        assignee_id = request.query_params.get('assignee')
        if not assignee_id:
            return Response({"error": "Assignee parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = UserTable.objects.get(id=assignee_id)
        except UserTable.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        now = timezone.now()
        today_end = now.replace(hour=23, minute=59, second=59)
        week_end = now + timedelta(days=(6 - now.weekday()))
        week_end = week_end.replace(hour=23, minute=59, second=59)
        tasks_due_today = Task.objects.filter(assignee=user, due_date__lte=today_end, status__in=['pending', 'in_progress', 'overdue']).order_by('due_date')
        tasks_due_this_week = Task.objects.filter(assignee=user, due_date__gt=today_end, due_date__lte=week_end, status__in=['pending', 'in_progress']).order_by('due_date')
        upcoming_tasks = Task.objects.filter(assignee=user, due_date__gt=week_end, status__in=['pending', 'in_progress']).order_by('due_date')
        completed_tasks = Task.objects.filter(assignee=user, status='completed').order_by('-completed_date')[:10]
        serializer_today = TaskSerializer(tasks_due_today, many=True)
        serializer_this_week = TaskSerializer(tasks_due_this_week, many=True)
        serializer_upcoming = TaskSerializer(upcoming_tasks, many=True)
        serializer_completed = TaskSerializer(completed_tasks, many=True)
        return Response({
            "due_today": serializer_today.data,
            "due_this_week": serializer_this_week.data,
            "upcoming": serializer_upcoming.data,
            "completed": serializer_completed.data
        })

class TaskCalendarView(APIView):
    def get(self, request):
        assignee_id = request.query_params.get('assignee')
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        if not assignee_id:
            return Response({"error": "Assignee parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = UserTable.objects.get(id=assignee_id)
        except UserTable.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        tasks_query = Task.objects.filter(assignee=user)
        if year and month:
            try:
                year = int(year)
                month = int(month)
                tasks_query = tasks_query.filter(due_date__year=year, due_date__month=month)
            except ValueError:
                return Response({"error": "Invalid year or month format"}, status=status.HTTP_400_BAD_REQUEST)
        tasks = tasks_query.order_by('due_date')
        serializer = TaskCalendarSerializer(tasks, many=True)
        calendar_data = {}
        for task in serializer.data:
            due_date = task['due_date'].split('T')[0]
            if due_date not in calendar_data:
                calendar_data[due_date] = []
            calendar_data[due_date].append(task)
        return Response(calendar_data)
