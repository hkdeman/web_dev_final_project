from django.shortcuts import render
from django.template import loader
from django.contrib.auth import authenticate,login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import json

from unevu.models import University, School

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
    context_dict = {}
    return render(request,'unevu/register.html', context=context_dict)

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
            