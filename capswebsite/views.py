from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'landing.html')

def loginPage(request):
    return render(request, 'login.html')

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