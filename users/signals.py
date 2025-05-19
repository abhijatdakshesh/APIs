from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Task, TaskSubmission

@receiver(pre_save, sender=Task)
def update_task_status(sender, instance, **kwargs):
    if instance.status != 'completed' and instance.due_date < timezone.now():
        instance.status = 'overdue'

@receiver(post_save, sender=TaskSubmission)
def mark_task_completed(sender, instance, created, **kwargs):
    if created:
        task = instance.task
        task.status = 'completed'
        task.completed_date = timezone.now()
        task.save(update_fields=['status', 'completed_date']) 