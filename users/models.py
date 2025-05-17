from django.db import models
from django.contrib.auth.models import User
import random
from django.utils import timezone
from datetime import timedelta

class UserTable(models.Model):
    # Basic Information
    phone_number = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    type = models.CharField(max_length=10, default='None')
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    aadhar_number = models.CharField(max_length=12, unique=True, null=True, blank=True)
    pan_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    
    # Address Information
    residential_address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pin_code = models.CharField(max_length=6, null=True, blank=True)
    
    # Employment Details
    total_experience_years = models.PositiveIntegerField(null=True, blank=True)
    is_currently_working = models.BooleanField(default=False)
    current_agencies = models.TextField(blank=True, null=True)
    
    # Profiling Information
    field_recovery_experience_years = models.PositiveIntegerField(null=True, blank=True)
    specialization_areas = models.JSONField(null=True, blank=True)  # Will store list of selected areas
    languages_known = models.JSONField(null=True, blank=True)  # Will store list of known languages
    
    # Document Uploads
    aadhaar_file = models.FileField(upload_to='documents/aadhaar/', null=True, blank=True)
    pan_file = models.FileField(upload_to='documents/pan/', null=True, blank=True)
    police_verification = models.FileField(upload_to='documents/police_verification/', null=True, blank=True)
    empanelment_letter = models.FileField(upload_to='documents/empanelment/', null=True, blank=True)
    
    # OTP Authentication
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.username} - {self.first_name} {self.last_name}"
        
    def generate_otp(self):
        """Generate a 6-digit OTP and save it to the user"""
        self.otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.otp_created_at = timezone.now()
        self.save()
        return self.otp
        
    def verify_otp(self, otp):
        """Verify if the provided OTP is valid"""
        # Check if OTP matches and is not expired (10 minutes validity)
        if self.otp and self.otp == otp and self.otp_created_at:
            otp_expiry = self.otp_created_at + timedelta(minutes=10)
            if timezone.now() <= otp_expiry:
                self.is_verified = True
                self.otp = None  # Clear OTP after successful verification
                self.save()
                return True
        return False
