from django.urls import path
from . import views


urlpatterns = [
    path('', views.user_login, name='login'),
    path('analisis', views.analisis, name='analisis'),
    path('register', views.register, name='register'),
    path('logout', views.user_logout, name='logout'),
    path('teacher/dashboard', views.dashboard_teacher, name='dashboard_teacher'),
    path('teacher/subject/<int:subject_id>/edit', views.edit_subject, name='edit_subject'),
    path('teacher/add_subject', views.add_subject, name='add_subject'),
    path('teacher/subject/<int:subject_id>/delete', views.delete_subject, name='delete_subject'),
    path('teacher/create_questionnaire/<int:subject_id>', views.create_questionnaire, name='create_questionnaire'),
    path('teacher/view_questionnaire/<int:subject_id>/', views.view_questionnaire, name='view_questionnaire'),
    path('teacher/view_detail/<int:questionnaire_id>', views.view_detail, name='view_detail'),
    path('teacher/question/<int:question_id>/edit', views.edit_question, name='edit_question'),
    path('teacher/feedback/<int:subject_id>', views.view_feedback, name='feedback'),
    path('student/dashboard', views.dashboard_student, name='dashboard_student'),
    path('student/answer_questionnaire/<int:questionnaire_id>', views.answer_questionnaire, name='answer_questionnaire'),
    path('student/view_summary/<int:subject_id>', views.view_summary, name='view_summary'),
    
]