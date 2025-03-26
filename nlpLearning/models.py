from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Sentiment_Analisis(models.Model):
    subject = models.CharField(max_length=100)
    comment = models.CharField(max_length=100)
    sentiment = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sentiment