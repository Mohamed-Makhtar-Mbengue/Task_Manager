# projects/forms.py
from django import forms
from .models import Project, Task, Comment, Attachment

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'members']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date', 'assigned_to', 'file', 'tags', 'dependencies']

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        if project:
            self.fields['assigned_to'].queryset = project.members.all()
            self.fields['dependencies'].queryset = Task.objects.filter(project=project)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']