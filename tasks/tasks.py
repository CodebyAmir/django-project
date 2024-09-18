from celery import shared_task
from django.utils.timezone import now
from .models import Task
from django.conf import settings

@shared_task
def send_task_reminder(task_id):
    task = Task.objects.get(id=task_id)
    if not task.completed and task.due_date > now():
        # Send reminder to the user (via email or any other method)
        print(f"Reminder: Task '{task.title}' is due at {task.due_date}")
        log_task_completion(task_id)

def log_task_completion(task_id):
    db = settings.MONGO_DB
    task = Task.objects.get(id=task_id)
    db.task_logs.insert_one({
        'task_id': task.id,
        'title': task.title,
        'due_date': task.due_date,
        'completed': task.completed,
    })
