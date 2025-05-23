from .models import Sentiment_Analisis, Subject, Questionnaire, Question, Choice, Answer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .utils.ml_function import text_process, model_pred
from django.core.files.storage import FileSystemStorage
from .forms import RegisterForm, CommentForm
from django.http import JsonResponse
from django.contrib import messages
import pandas as pd
import os

from django.forms import inlineformset_factory
from django.forms import modelform_factory
from django import forms

def home(request):
    return render(request, "pages/home.html")

def analisis(request):
    sentiment_anal = None
    if request.method == "POST":
        subject = request.POST.get("subject", "").strip()
        comment = request.POST.get("comment", "").strip()

        if subject and comment:
            comment_processed = text_process(comment)
            sentiment_anal = model_pred(comment_processed)
            sentiment_anal = "".join(sentiment_anal)

            text_sent = Sentiment_Analisis.objects.create(
                subject=subject, comment=comment, sentiment=sentiment_anal
            )
            text_sent.save()
            # analisis sentiment

    return render(request, "pages/analisis.html", {"result": sentiment_anal})

def user_login(request):

    if request.user.is_authenticated and request.user.role == "teacher":
        return redirect("teacher/dashboard")
    elif request.user.is_authenticated and request.user.role == "student":
        return redirect("student/dashboard")

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        print("POST data :", request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == "teacher":
                return redirect("teacher/dashboard")
            elif user.role == "student":
                return redirect("student/dashboard")
        else:
            print("Not Active user")
    else:
        form = AuthenticationForm()
    return render(request, "pages/login.html", {"form": form})

def register(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            if user.role == "teacher":
                return redirect("teacher/dashboard")
            elif user.role == "student":
                return redirect("student/dashboard")
    else:
        form = RegisterForm()
    return render(request, "pages/register.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("login")

def dashboard_teacher(request):
    if not request.user.is_authenticated:
        return redirect("login")

    subject = Subject.objects.filter(teacher=request.user).all()

    return render(
        request, "pages/teacher/teacher_dashboard.html", {"subjects": subject}
    )

def add_subject(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        subject_name = request.POST.get("subject_name", "").strip()
        if subject_name:
            subject = Subject.objects.create(name=subject_name, teacher=request.user)
            messages.success(request, "บันทึกข้อมูลสำเร็จ")
            return redirect("dashboard_teacher")
        else:
            messages.error(request, "กรุณากรอกชื่อวิชา")

    return render(request, "pages/teacher/teacher_dashboard.html")

def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == "POST":
        new_subject = request.POST.get("subject_name", "").strip()
        if new_subject:
            subject.name = new_subject
            subject.save()
            messages.success(request, "Subject updated successfully.")
            return redirect("dashboard_teacher")

    return render(request, "pages/teacher/edit_subject.html", {"subject": subject})

def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    return redirect("dashboard_teacher")

def create_questionnaire(request, subject_id):
    if not request.user.is_authenticated:
        return redirect("login")

    subject = Subject.objects.get(id=subject_id)
    choice = Choice.objects.filter(is_default=True)

    print(choice)

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        
        questionnaire = Questionnaire.objects.create(subject=subject, title=title)

        questions = request.POST.getlist("questions[]")
        types = request.POST.getlist("types[]")

        for i, question_text in enumerate(questions):
            q_type = types[i]
            question = Question.objects.create(
                questionnaire=questionnaire, text=question_text, type=q_type
            )
            if q_type == "choice":
                choice_key = f"choices_{i}[]"
                choices = request.POST.getlist(choice_key)
                for choice_text in choices:
                    if choice_text.strip():
                        choice = Choice.objects.create(
                            question=question, text=choice_text
                        )
        messages.success(request, "สร้างแบบสอบถามสําเร็จ")
        return redirect("dashboard_teacher")

    return render(
        request, "pages/teacher/create_questionnaire.html", {"subject": subject}
    )

def view_questionnaire(request, subject_id):
    if not request.user.is_authenticated:
        return redirect("login")

    subject = get_object_or_404(Subject, id=subject_id)
    questionnaires = Questionnaire.objects.filter(subject=subject)

    return render(
        request,
        "pages/teacher/view_questionnaire.html",    
        {"subject": subject, "questionnaires": questionnaires},
    )

def view_detail(request, questionnaire_id):
    if not request.user.is_authenticated:
        return redirect("login")

    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)

    return render(
        request,
        "pages/teacher/view_detail.html",
        {"questionnaire": questionnaire},
    )

def edit_question( request, question_id): 
    if not request.user.is_authenticated:
        return redirect("login")
    
    question = get_object_or_404(Question, id=question_id, questionnaire__subject__teacher=request.user)

    # ฟอร์มสำหรับคำถาม
    QuestionForm = modelform_factory(Question, fields=["text", "type"], widgets={
        'text' : forms.TextInput(attrs={'class': 'form-control'}),
        'type' : forms.Select(attrs={'class': 'form-select'})
    })
    
    # ถ้าเป็นคำถามแบบ choice จะมี formset สำหรับตัวเลือก
    ChoiceFormSet = inlineformset_factory(Question, Choice, fields=["text",], extra=0,  can_delete=True, widgets = {
      'text' : forms.TextInput(attrs={'class': 'form-control'})  
    })

    if request.method == "POST":
        form = QuestionForm(request.POST or None, instance=question)
        formset = ChoiceFormSet(request.POST or None, instance=question) if question.type == "choice" else None
        
        print("request.POST :", request.POST)   
        if form.is_valid() and (formset is None or formset.is_valid()):
            form.save()
            if formset:
                formset.save()
            messages.success(request, "แก้ไขคำถามเรียบร้อยแล้ว")
            return redirect("view_detail", questionnaire_id=question.questionnaire.id)
    else:
        form = QuestionForm(instance=question)
        formset = ChoiceFormSet(instance=question) if question.type == "choice" else None


    return render ( request, "pages/teacher/edit_question.html", {
        'form': form,
        'formset': formset,
        'questionnaire_id' : question.questionnaire.id
    })

def view_feedback(request, subject_id):
    if not request.user.is_authenticated:
        return redirect("login")

    subject = get_object_or_404(Subject, id=subject_id)
    comment = Sentiment_Analisis.objects.filter(subject=subject)

    return render(
        request,
        "pages/teacher/view_feedback.html",
        {"subject": subject, "feedbacks": comment},
    )

def dashboard_student(request):
    if not request.user.is_authenticated:
        return redirect("login")
    subjects = Subject.objects.all()
    return render(
        request,
        "pages/student/student_dashboard.html",
        {"subjects": subjects},
    )

def answer_questionnaire(request, questionnaire_id):
    if not request.user.is_authenticated:
        return redirect("login")

    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)

    if request.method == "POST":
        for question in questionnaire.questions.all():
            question_key = f'question_{question.id}'
            answer = request.POST.get(question_key)
            print(answer)
            if question.type == "choice":
                choice_id = request.POST.get(question_key)
                if choice_id:
                    choice = Choice.objects.get(id= choice_id)
                    Answer.objects.create(
                        question=question, choice=choice, student=request.user
                    )
            elif question.type == "text":
                text_answer = request.POST.get(question_key)
                if text_answer:
                    Answer.objects.create(
                        question=question, text_answer=text_answer, student=request.user
                    )
        messages.success(request, "บันทึกข้อมูลสําเร็จ")
        return redirect("dashboard_student")

    return render(
        request,
        "pages/student/answer_questionnaire.html",
        {"questionnaire": questionnaire},
    )

def view_summary(request, subject_id):
    if not request.user.is_authenticated:
        return redirect("login")

    subject = Subject.objects.get(id=subject_id)
    data_comment = Sentiment_Analisis.objects.filter(subject=subject)
    summary = {
        "total": data_comment.count(),
        "positive": data_comment.filter(sentiment="Positive").count(),
        "negative": data_comment.filter(sentiment="Negative").count(),
    }

    return render(
        request,
        "pages/student/view_summary.html",
        {"subject": subject, "comments": data_comment, "summary": summary},
    )

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
    if request.method == "POST" and request.FILES["file"]:
        upload_file = request.FILES["file"]
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
        if "Comment" in df.columns and "Subject" in df.columns:
            df["comment_process"] = df["Comment"].apply(text_process)
            df["sentiment"] = model_pred(df["comment_process"].tolist())
            subject_sumary = {}
            for index, row in df.iterrows():
                subject = row["Subject"]
                sentiment = row["sentiment"]
                if subject not in subject_sumary:
                    subject_sumary[subject] = {"total": 0, "positive": 0, "negative": 0}
                subject_sumary[subject]["total"] += 1
                if sentiment == "Positive":
                    subject_sumary[subject]["positive"] += 1
                else:
                    subject_sumary[subject]["negative"] += 1
            text = subject_sumary
    return render(request, "pages/upload.html", {"result": text})
