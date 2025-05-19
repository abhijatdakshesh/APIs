from rest_framework import serializers
from .models import UserTable
from django.utils import timezone
from datetime import timedelta
from .models import Task, TaskSubmission, TaskDocument

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

# Task Management Serializers (moved from tasks app)

class TaskDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDocument
        fields = ['id', 'document', 'document_type', 'upload_date']

class TaskSubmissionSerializer(serializers.ModelSerializer):
    documents = TaskDocumentSerializer(many=True, read_only=True)
    uploaded_files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )
    document_types = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True,
        required=False
    )
    class Meta:
        model = TaskSubmission
        fields = ['id', 'task', 'submitted_by', 'submission_date', 'notes', 'documents', 'uploaded_files', 'document_types']
        read_only_fields = ['submission_date']
    def create(self, validated_data):
        uploaded_files = validated_data.pop('uploaded_files', [])
        document_types = validated_data.pop('document_types', [])
        submission = TaskSubmission.objects.create(**validated_data)
        for i, file in enumerate(uploaded_files):
            document_type = document_types[i] if i < len(document_types) else None
            TaskDocument.objects.create(
                submission=submission,
                document=file,
                document_type=document_type
            )
        task = submission.task
        task.mark_as_completed()
        return submission

class TaskSerializer(serializers.ModelSerializer):
    submissions = TaskSubmissionSerializer(many=True, read_only=True)
    time_remaining = serializers.SerializerMethodField()
    due_category = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'assignee', 'assigner',
            'priority', 'status', 'created_date', 'due_date',
            'completed_date', 'location', 'tags', 'submissions',
            'time_remaining', 'due_category'
        ]
        read_only_fields = ['created_date', 'completed_date']
    def get_time_remaining(self, obj):
        if obj.status == 'completed':
            return "Completed"
        now = timezone.now()
        if obj.due_date < now:
            return "Overdue"
        delta = obj.due_date - now
        days = delta.days
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        return f"{days} days, {hours} hours, {minutes} minutes"
    def get_due_category(self, obj):
        if obj.status == 'completed':
            return "Completed"
        now = timezone.now()
        today_end = timezone.now().replace(hour=23, minute=59, second=59)
        this_week_end = now + timedelta(days=(6 - now.weekday()))
        this_week_end = this_week_end.replace(hour=23, minute=59, second=59)
        if obj.due_date <= today_end:
            return "Due Today"
        elif obj.due_date <= this_week_end:
            return "Due This Week"
        else:
            return "Upcoming"

class TaskCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'due_date', 'status', 'priority'] 