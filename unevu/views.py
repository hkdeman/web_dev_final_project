from django.shortcuts import render,redirect
from django.template import loader
from django.contrib.auth import authenticate,login,logout
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
    
    if ('submit' in request.POST):
        form = UserForm(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            
            user.set_password(password)
            user.save()
            
            registered = True
            
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('/')        

        else:
            print(form.errors)
    else:
        form = UserForm()

    return render(request,
                  'unevu/register.html',
                  {'form': form,
                   'registered': registered
                  })


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
    
        user = authenticate(email=email, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('unevu/home.html')
            else:
                return HttpResponse("Your Unevu account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(email, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'unevu/login.html', {})

def user_logout(request):
    logout(request)

    return redirect('/')

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