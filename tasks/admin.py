from django_celery_beat.models import PeriodicTask, IntervalSchedule
from datetime import timedelta
from .models import Task
from .tasks import send_task_reminder
import json

def create_reminder(task_id, due_date):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=5, period=IntervalSchedule.MINUTES)
    PeriodicTask.objects.create(
        interval=schedule,
        name=f'Task reminder {task_id}',
        task='tasks.tasks.send_task_reminder',
        args=json.dumps([task_id]),
        start_time=due_date - timedelta(hours=1),
    )

