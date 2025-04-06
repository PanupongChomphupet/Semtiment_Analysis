from django.shortcuts import render, redirect
from .utils.ml_function import text_process, model_pred
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import pandas as pd
import os
from .models import Sentiment_Analisis, Subject
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, CommentForm
from django.contrib.auth.forms import AuthenticationForm
# from .models import Sentiment_Analisis
# Create your views here.


def home(request):
    return render(request, 'pages/home.html')

def analisis(request):
    sentiment_anal = None
    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        comment = request.POST.get('comment', '').strip()
        
        if subject and comment:
            comment_processed = text_process(comment)
            sentiment_anal = model_pred(comment_processed)
            sentiment_anal = "".join(sentiment_anal)

            text_sent = Sentiment_Analisis.objects.create(subject=subject, comment=comment, sentiment = sentiment_anal)
            text_sent.save()
            # analisis sentiment 
            

    return render(request, 'pages/analisis.html', {'result': sentiment_anal})

def user_login(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        print("POST data :", request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'teacher':
                return redirect('teacher/dashboard')
            elif user.role == 'student':
                return redirect('student/dashboard')
        else :
            print("Not Active user")
    else:
        form = AuthenticationForm()
    return render(request, 'pages/login.html', {'form': form})

def register(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            if user.role == 'teacher':
                return redirect('teacher/dashboard')
            elif user.role == 'student':
                return redirect('student/dashboard')
    else:
        form = RegisterForm()
    return render(request, 'pages/register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def dashboard_teacher(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'pages/teacher/teacher_dashboard.html')

def dashboard_student(request):
    if not request.user.is_authenticated:
        return redirect('login')
    subject = Subject.objects.all()
    return render(request, 'pages/student/student_dashboard.html', {
        'subjects': subject
    })

def submint_comment(request, subject_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    subject = Subject.objects.get(id=subject_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            coment = form.cleaned_data['comment']
        print(subject, coment)        


    else:
        form = CommentForm()
    
    return render(request, 'pages/student/submit_comment.html', {
        'form': form,
        'subject': subject
    })

""" # data page
def apidata(request):
    text_sen = TextSent.objects.all()
    labels = []
    for text in text_sen:
        if text.subject not in labels:
            labels.append(text.subject)
            

        
    data = {
        "labels": labels,
        "datasets": [
            {
                "label": "จำนวนวิชา",
                "backgroundColor": "rgba(75, 192, 192, 0.2)",
                "borderColor": "rgba(75, 192, 192, 1)",
                "borderWidth": 1,
                "data": [10, 20, 30],
            }
        ]
    }
    return JsonResponse(data) """

def upload(request):
    text = []    
    if request.method == 'POST' and request.FILES['file']:
        upload_file = request.FILES['file']
        file = FileSystemStorage()
        file_path = file.path(upload_file.name)
        # มีไฟล์อยู่แล้วให้ลบ
        if os.path.exists(file_path):
            os.remove(file_path)
        # อัปโหลดใหม่
        file_path = file.save(upload_file.name, upload_file)
        file_url = file.path(file_path)
        # อ่านไฟล์
        df = pd.read_csv(file_url)
        if 'Comment' in df.columns and 'Subject' in df.columns:
            df['comment_process'] = df['Comment'].apply(text_process)
            df['sentiment'] = model_pred(df['comment_process'].tolist())
            subject_sumary = {}
            for index, row in df.iterrows():
                subject = row['Subject']
                sentiment = row['sentiment']
                if subject not in subject_sumary:
                    subject_sumary[subject] = {'total': 0, 'positive': 0, 'negative': 0}
                subject_sumary[subject]['total'] += 1
                if sentiment == 'Positive':
                    subject_sumary[subject]['positive'] += 1
                else:
                    subject_sumary[subject]['negative'] += 1
            text = subject_sumary
    return render(request, 'pages/upload.html', {'result': text})

