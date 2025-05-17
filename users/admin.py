from django.contrib import admin
from .models import UserTable

@admin.register(UserTable)
class UserTableAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'type', 'phone_number', 'email', 
                    'aadhar_number', 'pan_number', 'city', 'state', 'field_recovery_experience_years')
    search_fields = ('username', 'first_name', 'last_name', 'type', 'email', 'phone_number', 
                    'aadhar_number', 'pan_number', 'specialization_areas')
    list_filter = ('type', 'is_currently_working', 'state')
