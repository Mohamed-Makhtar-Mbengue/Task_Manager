from celery_config import shared_task
from django.utils import timezone
from .models import Task
from .utils import send_slack_notification # type: ignore

@shared_task
def send_task_reminders():
    tasks = Task.objects.filter(due_date__lte=timezone.now() + timezone.timedelta(hours=24), status__in=['todo', 'in_progress'])
    for task in tasks:
        message = f"Rappel : La tâche '{task.title}' est due le {task.due_date}."
        send_slack_notification(message)