from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    # path('upload', views.upload, name='upload'),
    # path('result', views.result, name='result'),
    path('analisis', views.analisis, name='analisis'),
    path('login', views.login, name='login'),
    # path('apidata', views.apidata, name='apidata'),
]