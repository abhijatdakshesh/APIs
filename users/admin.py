from django.contrib import admin
from .models import UserTable, Task, TaskSubmission, TaskDocument

@admin.register(UserTable)
class UserTableAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'type', 'phone_number', 'email', 
                    'aadhar_number', 'pan_number', 'city', 'state', 'field_recovery_experience_years')
    search_fields = ('username', 'first_name', 'last_name', 'type', 'email', 'phone_number', 
                    'aadhar_number', 'pan_number', 'specialization_areas')
    list_filter = ('type', 'is_currently_working', 'state')

# Task Management Admin (moved from tasks app)

class TaskDocumentInline(admin.TabularInline):
    model = TaskDocument
    extra = 1

class TaskSubmissionInline(admin.TabularInline):
    model = TaskSubmission
    extra = 0
    show_change_link = True

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assignee', 'priority', 'status', 'due_date', 'is_overdue')
    list_filter = ('status', 'priority', 'due_date')
    search_fields = ('title', 'description', 'assignee__username', 'assignee__first_name')
    date_hierarchy = 'due_date'
    inlines = [TaskSubmissionInline]
    def is_overdue(self, obj):
        return obj.is_overdue()
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue'

@admin.register(TaskSubmission)
class TaskSubmissionAdmin(admin.ModelAdmin):
    list_display = ('task', 'submitted_by', 'submission_date')
    list_filter = ('submission_date',)
    search_fields = ('task__title', 'submitted_by__username')
    inlines = [TaskDocumentInline]

@admin.register(TaskDocument)
class TaskDocumentAdmin(admin.ModelAdmin):
    list_display = ('submission', 'document_type', 'upload_date')
    list_filter = ('document_type', 'upload_date')
    search_fields = ('submission__task__title', 'document_type')
