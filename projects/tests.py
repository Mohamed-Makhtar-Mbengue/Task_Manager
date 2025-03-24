from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Project

User = get_user_model()

class ProjectTests(TestCase):
    def setUp(self):
        # Crée un utilisateur pour le créateur du projet
        self.creator = User.objects.create_user(
            username='testuser',
            password='testpass123',
        )
        # Crée un projet avec le créateur
        self.project = Project.objects.create(
            name='Test Project',
            description='This is a test project.',
            creator=self.creator,  # Assure-toi que ce champ est correct
        )

    def test_project_creation(self):
        self.assertEqual(self.project.name, 'Test Project')
        self.assertEqual(self.project.creator.username, 'testuser')

    def test_project_members(self):
        # Ajoute un membre au projet
        member = User.objects.create_user(
            username='memberuser',
            password='memberpass123',
        )
        self.project.members.add(member)
        self.assertIn(member, self.project.members.all())

    def test_project_str(self):
        self.assertEqual(str(self.project), 'Test Project')