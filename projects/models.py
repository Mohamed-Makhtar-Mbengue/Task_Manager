from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from Task import settings

User = get_user_model()

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True) 
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='projects',  # Nom de la relation inverse
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'À faire'),
        ('in_progress', 'En cours'),
        ('done', 'Terminé'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Basse'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
    ]

    project = models.ForeignKey('Project', related_name='tasks', on_delete=models.CASCADE, verbose_name="Projet")
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    timer_started_at = models.DateTimeField(null=True, blank=True)
    timer_stopped_at = models.DateTimeField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo', verbose_name="Statut")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name="Priorité")
    due_date = models.DateField(blank=True, null=True, verbose_name="Date d'échéance")
    assigned_to = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Assigné à")
    dependencies = models.ManyToManyField('self', symmetrical=False, blank=True, verbose_name="Dépendances")
    file = models.FileField(upload_to='task_files/', blank=True, null=True, verbose_name="Fichier joint")
    tags = models.CharField(max_length=200, blank=True, null=True, verbose_name="Tags")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tâche"
        verbose_name_plural = "Tâches"


class SubTask(models.Model):
    """
    Modèle pour représenter une sous-tâche.
    Une sous-tâche appartient à une tâche parente.
    """
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE, verbose_name="Tâche parente")
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    completed = models.BooleanField(default=False, verbose_name="Terminé")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Sous-tâche"
        verbose_name_plural = "Sous-tâches"


class Comment(models.Model):
    """
    Modèle pour représenter un commentaire.
    Un commentaire est associé à une tâche.
    """
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE, verbose_name="Tâche")
    author = models.CharField(max_length=100, verbose_name="Auteur")
    content = models.TextField(verbose_name="Contenu")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")

    def __str__(self):
        return f"Commentaire par {self.author} sur {self.task.title}"

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"


class Attachment(models.Model):
    """
    Modèle pour représenter un fichier joint.
    Un fichier joint est associé à une tâche.
    """
    task = models.ForeignKey(Task, related_name='attachments', on_delete=models.CASCADE, verbose_name="Tâche")
    file = models.FileField(upload_to='attachments/', verbose_name="Fichier")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de téléchargement")

    def __str__(self):
        return f"Fichier joint pour {self.task.title}"

    class Meta:
        verbose_name = "Fichier joint"
        verbose_name_plural = "Fichiers joints"