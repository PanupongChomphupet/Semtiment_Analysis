from .models import Sentiment_Analisis, CustomUser, Subject, Questionnaire, Question, Choice, Answer
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

# Register your models here.

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Sentiment_Analisis)
admin.site.register(Questionnaire)
admin.site.register(Question)
admin.site.register(Subject)
admin.site.register(Choice)
admin.site.register(Answer)

