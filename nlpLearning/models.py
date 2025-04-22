from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

# Create your models here.

# กำหนด Role Choices
ROLE_CHOICES = (
    ("teacher", "Teacher"),
    ("student", "Student"),
)

SENTIMENT_CHOICES = (
    ("positive", "Positive"),
    ("negative", "Negative"),
)


class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")

    def __str__(self):
        return self.username


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "teacher"},
    )

    def __str__(self):
        return self.name


class Questionnaire(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="questionnaires")
    title = models.CharField(max_length=100)
    # details = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class Question(models.Model):
    QUESTION_TYPES = (
        ("choice", "ตัวเลือก"),
        ("text", "ข้อความ"),
    )

    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=500)
    type = models.CharField(max_length=10, choices=QUESTION_TYPES)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices", blank=True, null=True)
    text = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "student"},
        null=True,
    )
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    text_answer = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"คำตอบของ {self.student.username} สำหรับคำถาม {self.question.id}"


class Sentiment_Analisis(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="comments"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "student"},
        null=True,
    )
    comment = models.TextField()
    sentiment = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
