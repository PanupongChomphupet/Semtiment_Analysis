from django.contrib import admin
from .models import Sentiment_Analisis, CustomUser, Subject
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.register(Sentiment_Analisis)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Subject)

