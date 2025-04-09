from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('analisis', views.analisis, name='analisis'),
    path('login', views.user_login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.user_logout, name='logout'),
    path('teacher/dashboard', views.dashboard_teacher, name='dashboard_teacher'),
    path('teacher/subject/<int:subject_id>/edit', views.edit_subject, name='edit_subject'),
    path('teacher/add_subject', views.add_subject, name='add_subject'),
    path('teacher/subject/<int:subject_id>/delete', views.delete_subject, name='delete_subject'),
    path('student/dashboard', views.dashboard_student, name='dashboard_student'),
    path('student/submit_comment/<int:subject_id>', views.submint_comment, name='submit_comment'),
    path('student/view_summary/<int:subject_id>', views.view_summary, name='view_summary'),
    
]