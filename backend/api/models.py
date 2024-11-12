from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('client', 'Client'),
]

class User(AbstractUser):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15)
    adresse = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    
    # Adding unique related names to avoid conflicts
    groups = models.ManyToManyField(Group, related_name="custom_user_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nom', 'prenom', 'telephone', 'adresse']
