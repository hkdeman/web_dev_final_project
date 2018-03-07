from django.shortcuts import render,redirect
from django.template import loader
from django.contrib.auth import authenticate,login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import json
from django.http import Http404
from unevu.forms import UserForm

from unevu.models import University, School, Course, Review, Teacher

def home(request):    
    context_dict = {}
    context_dict['universities'] = University.objects.all()
    
    response = render(request, 'unevu/home.html', context=context_dict)
    
    return response

def about(request):
    context_dict = {}
    
    response = render(request, 'unevu/about.html', context=context_dict)
    
    return response

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request,
                  'unevu/register.html',
                  {'form': user_form,
                   'registered': registered
                  })


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Unevu account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'unevu/login.html', {})

def choose_uni(request):
    context_dict = {}
    response = render(request, 'unevu/home.html', context=context_dict)
    return response
    
        
def home_details(request):
    if request.method == "POST":
        if request.POST.get("what")=="query-schools":
            name = request.POST.get('university')
            university = University.objects.get(name=name)
            schools = [school.name for school in School.objects.filter(university_id=university.id)]
            json_schools = json.dumps({"schools" : schools})
            return HttpResponse(json_schools, content_type ="application/json")
        elif request.POST.get("what")=="query-subjects":
            name = request.POST.get('university')
            school_name = request.POST.get('school')
            university = University.objects.get(name=name)
            school = School.objects.get(university_id=university.id,name=school_name)
            courses = [course.name for course in Course.objects.filter(school_id=school.id)]
            json_courses = json.dumps({"courses" : courses})
            return HttpResponse(json_courses, content_type ="application/json")
        elif request.POST.get("what")=="course-selected":
            name = request.POST.get('university')
            school_name = request.POST.get('school')
            course_name = request.POST.get('course')
            university = University.objects.get(name=name)
            school = School.objects.get(university_id=university.id,name=school_name)
            course = Course.objects.get(school_id=school.id,name=course_name)
            json_selected_course = json.dumps({"id" : course.id})
            return HttpResponse(json_selected_course, content_type ="application/json")

    return Http404("Course not found or access denied. Please go back.")


def review_course(request,course_id):
    course = Course.objects.get(id=course_id)
    teachers = [teacher.name for teacher in Teacher.objects.filter(school_id= course.school_id)]
    context_dict = {"title":course.name.title(),"description":course.description,"teachers":teachers}
    return render(request, 'unevu/subjects_review.html', context=context_dict)