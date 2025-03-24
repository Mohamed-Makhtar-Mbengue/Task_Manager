from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.auth import logout

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponse('Déconnexion réussie')
    else:
        return HttpResponse('Méthode non autorisée', status=405)

def profile(request):
    # Données du profil
    profile_data = {
        'name': 'John Doe',
        'function': 'Développeur Full Stack',
        'image_url': 'https://via.placeholder.com/100',
    }

    # Liste des tâches
    tasks = [
        {'id': 1, 'task': 'Développer la page de connexion', 'status': 'Terminé', 'date': '2023-10-01'},
        {'id': 2, 'task': 'Créer le tableau de bord', 'status': 'En cours', 'date': '2023-10-05'},
        {'id': 3, 'task': 'Configurer les tests unitaires', 'status': 'En attente', 'date': '2023-10-10'},
    ]

    return render(request, 'accounts/profile.html', {'profile': profile_data, 'tasks': tasks})

def custom_logout(request):
    if request.method == 'GET':
        logout(request)
        return redirect('home') 

def dashboard(request):
    return render(request, 'dashboard.html')