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
