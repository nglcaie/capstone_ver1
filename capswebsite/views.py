import email
from multiprocessing import context
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from .models import *
#from .forms import *
from datetime import datetime
from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
import os
from django.conf import settings
# Create your views here.
 
 
def index(request):
    return render(request, 'landing.html')
 
def loginPage(request):
    if request.user.is_authenticated and request.user.is_admin:
        return redirect('student_list')
    elif request.user.is_authenticated and request.user.is_student:
        return redirect('start_survey')
    else:
        if request.method == 'POST':
            email = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                users = request.user
                if user.is_authenticated and users.is_admin:
                    users.last_login = datetime.today()
                    users.save()
                    return redirect('student_list')
                elif user.is_authenticated and users.is_student:
                    users.last_login = datetime.today()
                    users.save()
                    return redirect('start_survey')
                else:
                    messages.error (request,'You have entered an invalid email or password.')
                    return render(request, 'login.html')
            else:
                    messages.error (request,'You have entered an invalid email or password.')
                    return render(request, 'login.html')
    return render(request, 'login.html')
 
def logout_view(request):
    logout(request)
    return redirect('login')
 
def sign_upPage(request):
    return render(request, 'sign_up.html')
 
def evaluation(request):
    return render(request, 'admin/evaluation.html')
 
def student_list(request):
    return render(request, 'admin/student_lists.html')
 
def student_answer(request):
    return render(request, 'admin/student_answer.html')
 
def answer_summary(request):
    return render(request, 'student/answer_summary.html')
 
def start_survey(request):
    return render(request, 'student/start_survey.html')
 
def survey_question(request):
    return render(request, 'student/survey_question.html')
 
def student_navbar(request):
    return render(request, 'student/student-navbar.html')
 
def thankyou(request):
    return render(request, 'student/thankyou.html')

def admin_navbar(request):
    return render(request, 'admin/admin_navbar.html')