from django.shortcuts import render, get_object_or_404
from .models import Notification

def notification_list(request):
    notifications = Notification.objects.all()
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})

def notification_detail(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    return render(request, 'notifications/notification_detail.html', {'notification': notification})