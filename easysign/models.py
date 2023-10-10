from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms

class User(AbstractUser):
    user_api_key = models.CharField(max_length=200)
    def __str__(self):
        return self.first_name

class Document(models.Model):
    doc_id = models.CharField(max_length=500)
    original_content = models.TextField()
    hindi_content = models.TextField(blank=True, null=True)
    spanish_content = models.TextField(blank=True, null=True)
    chinese_content = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
