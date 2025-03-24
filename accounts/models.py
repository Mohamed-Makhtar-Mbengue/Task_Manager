from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Ajoute tes champs personnalisés ici (si nécessaire)
    bio = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    # Ajoute des related_name uniques pour éviter les conflits
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='accounts_user_set',  # Nom unique pour la relation inverse
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='accounts_user_set',  # Nom unique pour la relation inverse
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )