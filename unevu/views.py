from django.shortcuts import render,redirect
from django.template import loader
from django.contrib.auth import authenticate,login,logout, get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import json
from django.http import Http404
from unevu.forms import UserForm

from unevu.models import *

def home(request):    
    context_dict = {}
    context_dict['universities'] = University.objects.all()
    context_dict['top_unis'] = University.objects.order_by('-avgRating')[:5]
    context_dict['top_courses'] = Course.objects.order_by('-avgRating')[:5]
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
            
            if registered:
                u = User.objects.get(username=username)
                UserProfile.objects.create(user_id=u.id)

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
        if 'home' in request.POST:
           return HttpResponseRedirect('/')
        elif 'submit' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
    
            user = authenticate(username=username, password=password)
            if user is None:
                User = get_user_model()
                user_queryset = User.objects.all().filter(email__iexact=username)
                if user_queryset:
                    username = user_queryset[0].username
                    user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.POST.get('remember_me'):
                        request.session.set_expiry(settings.KEEP_LOGGED_DURATION)
                    
                    #Once logged in go back to home page    
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponse("Your Unevu account is disabled.")
            else:
                print("Invalid login details: {0}, {1}".format(username, password))
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
    
def uni_details(request):
    if request.method == "POST":
        if request.POST.get("what")=="query-schools":
            name = request.POST.get('university')
            university = University.objects.get(name=name)
            json_university = json.dumps({"id" : university.id})
            return HttpResponse(json_university, content_type ="application/json")

def university(request,uni_id):
    if request.method == "GET":
        university = University.objects.get(id=uni_id)
        schools = [school.name for school in School.objects.filter(university_id=university.id)]
        rating = None
        uni_desc = university.description
        uni_reviews = UniReview.objects.filter(university=university).order_by('-rating')[:3]
        if request.user.is_authenticated:
            likes = Like.objects.filter(username = request.user)
            likes = [ like.review_id for like in likes]
            for review in uni_reviews:
                if review.id in likes:
                    review.liked = True
                else:
                    review.liked = False
        try:
            rating = round(sum([int(review.rating) for review in uni_reviews])/len(uni_reviews),1)
        except:
            pass

        context_dict = {"schools":schools,"university":university,"rating":rating, "reviews": uni_reviews}
        response = render(request, 'unevu/university.html', context=context_dict)
        return response

def school_details(request):
    if request.method == "POST":
        if request.POST.get("what")=="query-subjects":
            id = int(request.POST.get('university'))
            school_name = request.POST.get('school')
            university = University.objects.get(id=id)
            school = School.objects.get(university_id=university.id,name=school_name)
            courses = [course.name for course in Course.objects.filter(school_id=school.id)]
            json_courses = json.dumps({"info" : courses})
            return HttpResponse(json_courses, content_type ="application/json")
        elif request.POST.get("what")=="query-teachers":
            id = int(request.POST.get('university'))
            school_name = request.POST.get('school')
            university = University.objects.get(id=id)
            school = School.objects.get(university_id=university.id,name=school_name)
            teachers = [teacher.name for teacher in Teacher.objects.filter(school_id=school.id) if teacher.email and teacher.mobile and teacher.imageUrl]
            json_courses = json.dumps({"info" : teachers})
            return HttpResponse(json_courses, content_type ="application/json")
        elif request.POST.get("what")=="course-selected":
            id = int(request.POST.get('university'))
            school_name = request.POST.get('school')
            course_name = request.POST.get('course')
            university = University.objects.get(id=id)
            school = School.objects.get(university_id=university.id,name=school_name)
            course = Course.objects.get(school_id=school.id,name=course_name)
            json_selected_course = json.dumps({"id" : course.id})
            return HttpResponse(json_selected_course, content_type ="application/json")
        elif request.POST.get("what")=="teacher-selected":
            id = int(request.POST.get('university'))
            school_name = request.POST.get('school')
            teacher_name = request.POST.get('teacher')
            university = University.objects.get(id=id)
            school = School.objects.get(university_id=university.id,name=school_name)
            teacher = Teacher.objects.get(school_id=school.id,name=teacher_name)
            json_selected_course = json.dumps({"id" : teacher.id})
            return HttpResponse(json_selected_course, content_type ="application/json")

    return Http404("Course not found or access denied. Please go back.")


def review_course(request,course_id):
    if request.method == "GET":
        course = Course.objects.get(id=course_id)
        teachers = [teacher.name for teacher in Teacher.objects.filter(school_id= course.school_id)]
        reviews = CourseReview.objects.filter(course=course)
        teacher = course.convener
        if request.user.is_authenticated:
            likes = Like.objects.filter(username = request.user)
            likes = [ like.review_id for like in likes]
            for review in reviews:
                if review.id in likes:
                    review.liked = True
                else:
                    review.liked = False
        context_dict = {"title":course.name.title(),"description":course.description,"teachers":teachers,"teacher":teacher,
                        "reviews":reviews, "uni_name":course.school.university.name,"uni_id":course.school.university.id}
        return render(request, 'unevu/subjects_review.html', context=context_dict)
    elif request.method == "POST":
        if request.user.is_authenticated:
            what = request.POST.get('what')
            if what == "update-teacher":
                teacher_name = request.POST.get('teacher')
                course = Course.objects.get(id=course_id)
                teacher = Teacher.objects.get(name=teacher_name,school=course.school)
                requests = [request.username for request in Request.objects.filter(course=course)]
                if request.user in requests:
                    return HttpResponse("Exists")
                request = Request.objects.create(username=request.user,course=course,teacher=teacher,status=False)
                request.save()
                return HttpResponse("Success")

def add_review(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            what = request.POST.get('what')
            if what == "course":
                course_id = request.POST.get('course')
                review = request.POST.get('review')
                rating = request.POST.get('rating')
                course = Course.objects.get(id=int(course_id))
                course.avgRating  = (course.avgRating * course.noOfRatings + int(rating))/(course.noOfRatings+1)
                course.noOfRatings = course.noOfRatings+1
                course.save()
                course_review = CourseReview.objects.create(course=course,username=request.user,reviewText=review,rating=rating)
                course_review.save()
                return HttpsResponse("success")                
            elif what == "university":
                uni_id = request.POST.get('university')
                review = request.POST.get('review')
                rating = request.POST.get('rating')
                university = University.objects.get(id = int(uni_id))
                university.avgRating  = (university.avgRating * university.noOfRatings + int(rating))/(university.noOfRatings+1)
                university.noOfRatings = university.noOfRatings+1
                university.save()
                uni_review = UniReview.objects.create(university=university,username=request.user,reviewText=review,rating=rating)
                uni_review.save()
                return HttpsResponse("success")
            elif what == "teacher":
                uni_id = request.POST.get('teacher')
                review = request.POST.get('review')
                rating = request.POST.get('rating')
                teacher = Teacher.objects.get(id = int(uni_id))
                teacher.avgRating  = (teacher.avgRating * teacher.noOfRatings + int(rating))/(teacher.noOfRatings+1)
                teacher.noOfRatings = teacher.noOfRatings+1
                teacher.save()
                teacher_review = TeacherReview.objects.create(teacher=teacher,username=request.user,reviewText=review,rating=rating)
                teacher_review.save()
                return HttpsResponse("success")
    else:
        return HttpResponse("Error")



def review_uni(request,uni_id):
    university = University.objects.get(id=uni_id)
    reviews = UniReview.objects.filter(university=university)
    likes = None
    if request.user.is_authenticated:
        likes = Like.objects.filter(username = request.user)
        likes = [ like.review_id for like in likes]
        for review in reviews:
            if review.id in likes:
                review.liked = True
            else:
                review.liked = False
    context_dict = {"title":university.name.title(),"description":university.description,
                    "reviews":reviews,"lat":university.lat,"lng":university.lng,"uni_id":university.id}
    return render(request, 'unevu/universities_review.html', context=context_dict)

def review_teacher(request,teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    reviews = TeacherReview.objects.filter(teacher=teacher)
    if request.user.is_authenticated:
        likes = Like.objects.filter(username = request.user)
        likes = [ like.review_id for like in likes]
        for review in reviews:
            if review.id in likes:
                review.liked = True
            else:
                review.liked = False
    context_dict = {"teacher":teacher, "reviews":reviews, "uni_name":teacher.school.university.name,"uni_id":teacher.school.university.id}
    return render(request, 'unevu/teachers_review.html', context=context_dict)

def like(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            username = request.user
            review_id = int(request.POST.get('id'))
            user = User.objects.get(username=username)
            review = Review.objects.get(id=review_id)
            like_review, created = Like.objects.get_or_create(username=user,review=review)
            json_selected_course = None
            if created:
                like_review.save()
                review.likes+=1
                json_selected_course = json.dumps({"what" : "like"})
            else:
                Like.objects.get(username=user,review=review).delete()
                review.likes-=1
                json_selected_course = json.dumps({"what" : "unlike"})            
            review.save()            
            return HttpResponse(json_selected_course, content_type ="application/json")
        else:
            return Http404("Cannot like without logged in")


def preferences(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            reviews = None
            reviews = Review.objects.filter(username_id=request.user.id)     
            likes = Like.objects.filter(username = request.user)
            likes = [ like.review_id for like in likes]
            for review in reviews:
                if review.id in likes:
                    review.liked = True
                else:
                    review.liked = False
            context_dict = {"reviews":reviews}
            return render(request, 'unevu/preferences.html', context=context_dict)
        elif request.method == "POST":
            what = request.POST.get('what')
            if what == "delete-account":
                request.user.delete()
                return HttpResponse("success")
            elif what == "update-details":
                first_name = request.POST.get("first_name")
                last_name = request.POST.get("last_name")
                request.user.first_name = first_name
                request.user.last_name = last_name
                request.user.save()
                return HttpResponse("success")
    else:
        return HttpResponseRedirect('/')

def update_review(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            what = request.POST.get('what')
            if what == "update":    
                id = request.POST.get('id')
                reviewText = request.POST.get('review')
                rating = request.POST.get('rating')
                review = Review.objects.get(id=id)
                review.reviewText = reviewText
                review.rating = rating
                review.save()
                return HttpResponse("success")
            if what == "delete":
                id = request.POST.get('id')
                review = Review.objects.get(id=id)
                review.delete()
                return HttpResponse("success")                
                                
