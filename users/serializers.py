from rest_framework import serializers
from .models import UserTable

class MetadataSerializer(serializers.Serializer):
    field_recovery_experience_years = serializers.IntegerField(required=True)
    specialization_areas = serializers.JSONField(required=True)
    languages_known = serializers.JSONField(required=True)
    
    class Meta:
        fields = ('field_recovery_experience_years', 'specialization_areas', 'languages_known')

class UserRegistrationSerializer(serializers.ModelSerializer):
    metadata = MetadataSerializer(write_only=True)
    
    class Meta:
        model = UserTable
        fields = (
            'username', 'first_name', 'last_name', 'type', 'email', 'phone_number', 
            'date_of_birth', 'aadhar_number', 'pan_number',
            'residential_address', 'city', 'state', 'pin_code', 
            'total_experience_years', 'is_currently_working', 'current_agencies',
            'metadata'
        )
        extra_kwargs = {
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'type': {'required': True},
            'email': {'required': True},
            'phone_number': {'required': True},
            'date_of_birth': {'required': True},
            'aadhar_number': {'required': True},
            'pan_number': {'required': True},
            'residential_address': {'required': True},
            'city': {'required': True},
            'state': {'required': True},
            'pin_code': {'required': True},
            'total_experience_years': {'required': True},
            'is_currently_working': {'required': True},
            'current_agencies': {'required': True},
        }

    def create(self, validated_data):
        # Extract and remove metadata from validated data
        metadata = validated_data.pop('metadata')
        
        # Create UserTable with all fields
        user = UserTable.objects.create(
            **validated_data,
            field_recovery_experience_years=metadata.get('field_recovery_experience_years'),
            specialization_areas=metadata.get('specialization_areas'),
            languages_known=metadata.get('languages_known')
        )
        return user

class DocumentUploadSerializer(serializers.Serializer):
    aadhaar_file = serializers.FileField(required=False)
    pan_file = serializers.FileField(required=False)
    police_verification = serializers.FileField(required=False)
    empanelment_letter = serializers.FileField(required=False)
    
    def validate(self, attrs):
        """Validate that at least one document is being uploaded"""
        if not any(attrs.values()):
            raise serializers.ValidationError("At least one document must be uploaded")
        return attrs

class OTPRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    
    def validate_phone_number(self, value):
        """Validate that the phone number exists in the database"""
        try:
            UserTable.objects.get(phone_number=value)
        except UserTable.DoesNotExist:
            raise serializers.ValidationError("No user found with this phone number")
        return value

class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)
    
    def validate(self, attrs):
        """Validate that the phone number exists"""
        phone_number = attrs.get('phone_number')
        try:
            UserTable.objects.get(phone_number=phone_number)
        except UserTable.DoesNotExist:
            raise serializers.ValidationError("No user found with this phone number")
        return attrs 