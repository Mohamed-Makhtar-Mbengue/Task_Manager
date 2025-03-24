from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('<int:project_id>/create_task/', views.create_task, name='create_task'),
    path('task/<int:task_id>/update_status/', views.update_task_status, name='update_task_status'),
    path('task/<int:task_id>/add_subtask/', views.add_subtask, name='add_subtask'),
    path('task/<int:task_id>/start_timer/', views.start_timer, name='start_timer'),
    path('task/<int:task_id>/stop_timer/', views.stop_timer, name='stop_timer'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/update_status/', views.update_task_status, name='update_task_status'),
    path('task/<int:task_id>/add_subtask/', views.add_subtask, name='add_subtask'),
    path('registration/login.html', views.login_view, name='login_html'),
    path('registration/register.html', views.register_view, name='register_html'),
    path('accounts/profile/', views.profile, name='profile'),
]