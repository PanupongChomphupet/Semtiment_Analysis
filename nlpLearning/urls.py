from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('analisis', views.analisis, name='analisis'),
    path('login', views.user_login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.user_logout, name='logout'),
    path('teacher/dashboard', views.dashboard_teacher, name='dashboard_teacher'),
    path('student/dashboard', views.dashboard_student, name='dashboard_student'),
    path('student/submit_comment/<int:subject_id>', views.submint_comment, name='submit_comment'),
]