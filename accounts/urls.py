from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registration/register.html', views.register, name='register_html'),
    path('registration/login.html', views.login, name='login_html'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]