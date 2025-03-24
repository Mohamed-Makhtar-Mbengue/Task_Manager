from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Project, Task, Comment, Attachment,SubTask
from .forms import ProjectForm, TaskForm, CommentForm, AttachmentForm

def project_list(request):
    projects = Project.objects.filter(members=request.user)
    return render(request, 'projects/project_list.html', {'projects': projects})

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = project.tasks.all()
    return render(request, 'projects/project_detail.html', {'project': project, 'tasks': tasks})

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()
            form.save_m2m()  # Nécessaire pour enregistrer les membres (ManyToManyField)
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()
    return render(request, 'projects/create_project.html', {'form': form})

def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Projet mis à jour avec succès.")
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/edit_project.html', {'form': form, 'project': project})

def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Projet supprimé avec succès.")
        return redirect('project_list')
    return render(request, 'projects/confirm_delete_project.html', {'project': project})

def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            form.save_m2m()
            messages.success(request, "Tâche créée avec succès.")
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm(project=project)
    return render(request, 'projects/create_task.html', {'form': form, 'project': project})

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task, project=task.project)
        if form.is_valid():
            form.save()
            messages.success(request, "Tâche mise à jour avec succès.")
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskForm(instance=task, project=task.project)
    return render(request, 'projects/edit_task.html', {'form': form, 'task': task})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, "Tâche supprimée avec succès.")
        return redirect('project_detail', project_id=task.project.id)
    return render(request, 'projects/confirm_delete_task.html', {'task': task})

def add_comment(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            messages.success(request, "Commentaire ajouté avec succès.")
            return redirect('task_detail', task_id=task.id)
    else:
        form = CommentForm()
    return render(request, 'projects/add_comment.html', {'form': form, 'task': task})

def add_attachment(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.task = task
            attachment.uploaded_by = request.user
            attachment.save()
            messages.success(request, "Pièce jointe ajoutée avec succès.")
            return redirect('task_detail', task_id=task.id)
    else:
        form = AttachmentForm()
    return render(request, 'projects/add_attachment.html', {'form': form, 'task': task})

def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('nom_de_la_vue_liste_des_taches')

def add_subtask(request, task_id):
    task = get_object_or_404(Task, id=task_id) 
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        SubTask.objects.create(
            task=task,
            title=title,
            description=description,
            completed=False
        )
        return redirect('nom_de_la_vue_detail_task', task_id=task.id)
    return render(request, 'projects/add_subtask.html', {'task': task})

def start_timer(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.timer_started_at = timezone.now()
    task.save()
    return redirect('views.py') 

def stop_timer(request, task_id):
   task = get_object_or_404(Task, id=task_id)
   if task.timer_started_at:
        task.timer_stopped_at = timezone.now()
        task.duration = (task.timer_stopped_at - task.timer_started_at).total_seconds()  # Durée en secondes
        task.save()
        return redirect('views.py')
   
def dashboard(request):
    projects = Project.objects.all()
    tasks = Task.objects.all()
    context = {
        'projects': projects,
        'tasks': tasks,
    }
    return render(request, 'projects/dashboard.html', context)

def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    context = {
        'task': task,
    }
    return render(request, 'projects/task_detail.html', context)

def home(request):
     return render(request, 'home.html')

def login_view(request):
     return render(request, 'registration/login.html')

def register_view(request):
    return render(request, 'registration/register.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def profile(request):
    return render(request, 'profile.html')

def custom_logout(request):
    logout(request)  
    return redirect('login')