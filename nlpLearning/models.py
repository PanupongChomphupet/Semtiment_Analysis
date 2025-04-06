from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.

# กำหนด Role Choices
ROLE_CHOICES = (
    ('teacher', 'Teacher'),
    ('student', 'Student'),
)

SENTIMENT_CHOICES = (
    ('positive', 'Positive'),
    ('negative', 'Negative'),
)

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'}
    )
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return self.username

class Sentiment_Analisis(models.Model):
    subject = models.CharField(max_length=100)
    comment = models.CharField(max_length=100)
    sentiment = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sentiment
    
