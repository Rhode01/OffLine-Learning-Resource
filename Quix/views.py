import os
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Category,Subjects,Question,Learning_Resources,Learning_Resource_Subject,Learning_Resource_Category,UserAnswer,Answer,UserProgress
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
def landing_page(request):
    return HttpResponse(render(request, 'landing_page.html'))
def Home(self):
        return HttpResponse("in production")
def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('dashboard')
        else:
            messages.info(request, "incorrate username or password")
            return HttpResponseRedirect('login')
    return HttpResponse(render(request, 'login_page.html'))
def signup_page(request):
    if request.method == "POST":
        username = request.POST['username']
        # email = request.POST['email']
        pswd1 = request.POST['pswd1']
        pswd2 = request.POST['pswd2']
        if pswd1 == pswd2:
            if User.objects.all().filter(username=username).exists():
                messages.warning(request,'Username Already Exists')
                
                return HttpResponseRedirect('login')
            else:
                new_user = User.objects.create_user(username, password=pswd1)
                new_user.save();
                messages.success(request,"Successfully create an account please, login now")
                return HttpResponseRedirect('login')
        else:
            messages.warning(request,'password doesnt match')
            return HttpResponseRedirect('login')
    
    else:
        return HttpResponse(render(request, 'login_page.html'))
    
def logout_view(request):
        logout(request)
        return HttpResponseRedirect('login')
def dashboard(request):
    return HttpResponse(render(request,'dashboard.html'))

def exams_list(request):
    exams_category = Category.EXAM_CHOICES
    return render(request, 'exam_lists.html', {'exams_category': exams_category})
def exams_category(request,exams_choice):
        category = Category.objects.get(name=exams_choice)  
        subjects = Subjects.objects.filter(category=category)
        
        context = {
            'subjects': subjects,
            'choice': category
        }
        return render (request,'exam_lists.html',context)
def subject_questions(request, category, subject):
    questions_category = Category.objects.get(name=category)
    questions_subject = Subjects.objects.filter(name=subject)
    questions = Question.objects.filter(exam_category=questions_category, subject__in=questions_subject)

    page_number = request.GET.get('page')
    paginator = Paginator(questions, 3)
    question = paginator.get_page(page_number)

    remaining_questions = paginator.count - (question.number - 1) * paginator.per_page
    next_button = remaining_questions > paginator.per_page
    
    context = {
        'category': category,
        'subject': subject,
        'questions': question,
        'remaining_questions': remaining_questions,
        'has_previous': question.has_previous(),
        'has_next': question.has_next(),
        'previous_page_number': question.previous_page_number() if question.has_previous() else None,
        'next_page_number': question.next_page_number() if question.has_next() else None,
        'next_button': next_button,
    }
    return render(request, "questions.html", context)

def learning_resources_subjects(request,category):
    learning_category = Learning_Resource_Category.objects.get(name=category)  
    subjects = Learning_Resource_Subject.objects.filter(category=learning_category)
    context = {
        'subjects': subjects,
        'category': learning_category
    }
    return render (request,'resource_subject.html',context)
def learning_resources(request):
    resource_catego = Learning_Resource_Category.RESOURCE_CHOICES
    context ={
         'category': resource_catego,
    }
    return render(request,"resources.html", context)
def open_subject_resources(request,category,subject):
    resource_category = Learning_Resource_Category.objects.get(name=category)
    resource_subject = Learning_Resource_Subject.objects.filter(name=subject)
    learning_resource = Learning_Resources.objects.filter(category=resource_category,subject__in=resource_subject)

    page_number = request.GET.get('page')
    paginator = Paginator(learning_resource, 5)
    resources = paginator.get_page(page_number)

    remaining_questions = paginator.count - (resources.number - 1) * paginator.per_page
    next_button = remaining_questions > paginator.per_page
    

    
    context ={
        'resource':resources,
        'has_previous': resources.has_previous(),
        'has_next': resources.has_next(),
        'previous_page_number': resources.previous_page_number() if resources.has_previous() else None,
        'next_page_number': resources.next_page_number() if resources.has_next() else None,
    }
    return render(request,'resource_display.html', context)

def show_video(request,id):
    resource = Learning_Resources.objects.get(pk=id)
    video_url = resource.file.url
    return render(request, 'index.html', {
        'video_url': video_url,
    })

def handle_user_answers(request):
    username = request.user.username
    if request.method =="POST":
         answers = request.POST.getlist('answer')
         question_ids = request.POST.getlist('question_id')
         questions = request.POST.getlist('question')
         for answer,question,question_id in zip(answers,questions,question_ids):
                handle_user_score(question_id,answer,username)
    return HttpResponse("working")
def handle_user_score(question_id,answer,username):
    current_answer = Answer.objects.filter(question=question_id).first()
    userScore =0
    if current_answer:
        answer_text = current_answer.answer
        if(answer_text == answer):
            userScore +=1
            # answered = UserAnswer.objects.create(question=question, answer=answer, user=username)
        else:
            print("Thats not the correct Answer please try again")
    else:
        print("No answer found for the current question ID")
@login_required
def user_progress(request):
    user = request.user
    scores = UserProgress.objects.filter(user=user)

    subjects = scores.values_list('subjects__name', flat=True).distinct()
    # categories = scores.values_list('exam__category__name', flat=True).distinct()
    exams = scores.values_list('exam__name', flat=True).distinct()

    context ={
         'subject':subjects,
         'score':exams
    }



    return HttpResponse(render(request,'userProgress.html'))
   

       