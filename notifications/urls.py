# notifications/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Définis tes URLs ici
    path('', views.notification_list, name='notification_list'),
    path('<int:notification_id>/', views.notification_detail, name='notification_detail'),
]