from django.shortcuts import render,redirect
from django.template import loader
from django.contrib.auth import authenticate,login,logout, get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import json
from django.http import Http404
from unevu.forms import UserForm

from unevu.models import *

#Displays home page
def home(request):    
    context_dict = {}
    context_dict['universities'] = University.objects.all()
    context_dict['top_unis'] = University.objects.order_by('-avgRating')[:5]
    context_dict['top_courses'] = Course.objects.order_by('-avgRating')[:5]
    response = render(request, 'unevu/home.html', context=context_dict)
    
    return response

#Displays about page
def about(request):
    context_dict = {}
    
    response = render(request, 'unevu/about.html', context=context_dict)
    
    return response

#Displays registration page
def register(request):
    registered = False
    
    #Submission of registration form
    if ('submit' in request.POST):
        form = UserForm(data=request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            
            #Setting password and saving the user to the database
            user.set_password(password)
            user.save()
            
            registered = True
            
            #Login
            if registered:
                u = User.objects.get(username=username)
                UserProfile.objects.create(user_id=u.id)
            
            #If success in logging in redirect to home page
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

#Displays login page
def user_login(request):
    if request.method == 'POST':
        #Redirects to home page without logging in
        if 'home' in request.POST:
           return HttpResponseRedirect('/')
        #User logs in
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
                    #Keep logged in
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

#Allows user to log out
def user_logout(request):
    logout(request)

    return redirect('/')

#Get schools for each university    
def uni_details(request):
    if request.method == "POST":
        if request.POST.get("what")=="query-schools":
            name = request.POST.get('university')
            university = University.objects.get(name=name)
            json_university = json.dumps({"id" : university.id})
            return HttpResponse(json_university, content_type ="application/json")

#Display the university page
def university(request,uni_id):
    if request.method == "GET":
        university = University.objects.get(id=uni_id)
        schools = [school.name for school in School.objects.filter(university_id=university.id)]
        rating = None
        uni_desc = university.description
        uni_reviews = UniReview.objects.filter(university=university).order_by('-rating')[:3]
        #Get likes only if logged in  
        if request.user.is_authenticated:
            likes = Like.objects.filter(username = request.user)
            likes = [ like.review_id for like in likes]
            for review in uni_reviews:
                if review.id in likes:
                    review.liked = True
                else:
                    review.liked = False
        try:
            #Get average rating for university    
            rating = round(sum([int(review.rating) for review in uni_reviews])/len(uni_reviews),1)
        except:
            pass

        context_dict = {"schools":schools,"university":university,"rating":rating, "reviews": uni_reviews}
        response = render(request, 'unevu/university.html', context=context_dict)
        return response

#Get choices for school selected 
def school_details(request):
    if request.method == "POST":
        #Get subjects available   
        if request.POST.get("what")=="query-subjects":
            id = int(request.POST.get('university'))
            school_name = request.POST.get('school')
            university = University.objects.get(id=id)
            school = School.objects.get(university_id=university.id,name=school_name)
            courses = [course.name for course in Course.objects.filter(school_id=school.id)]
            json_courses = json.dumps({"info" : courses})
            return HttpResponse(json_courses, content_type ="application/json")
        #Get teachers available           
        elif request.POST.get("what")=="query-teachers":
            id = int(request.POST.get('university'))
            school_name = request.POST.get('school')
            university = University.objects.get(id=id)
            school = School.objects.get(university_id=university.id,name=school_name)
            teachers = [teacher.name for teacher in Teacher.objects.filter(school_id=school.id) if teacher.email and teacher.mobile and teacher.imageUrl]
            json_courses = json.dumps({"info" : teachers})
            return HttpResponse(json_courses, content_type ="application/json")
        #Get course selected   
        elif request.POST.get("what")=="course-selected":
            id = int(request.POST.get('university'))
            school_name = request.POST.get('school')
            course_name = request.POST.get('course')
            university = University.objects.get(id=id)
            school = School.objects.get(university_id=university.id,name=school_name)
            course = Course.objects.get(school_id=school.id,name=course_name)
            json_selected_course = json.dumps({"id" : course.id})
            return HttpResponse(json_selected_course, content_type ="application/json")
        #Get teacher selected           
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

#Display Course page
def review_course(request,course_id):
    if request.method == "GET":
        course = Course.objects.get(id=course_id)
        teachers = [teacher.name for teacher in Teacher.objects.filter(school_id= course.school_id)]
        reviews = CourseReview.objects.filter(course=course)
        teacher = course.convener
        if request.user.is_authenticated:
            #Show likes on reviews if logged in
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
            #Request to assign teacher to admin
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

#Allows to add reviews on models
def add_review(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            what = request.POST.get('what')
            #Add course review
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
            #Add uni review             
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
            #Add teacher review
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


#Display all reviews for a university (View All)
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

#Display all reviews for a teacher (View All)
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

#Allows liking
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


#Allows a user to change their name or delete their account
def preferences(request):
    #Display preferences
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
            #delete account
            if what == "delete-account":
                request.user.delete()
                return HttpResponse("success")
            #update user details (first name, last name)
            elif what == "update-details":
                first_name = request.POST.get("first_name")
                last_name = request.POST.get("last_name")
                request.user.first_name = first_name
                request.user.last_name = last_name
                request.user.save()
                return HttpResponse("success")
    else:
        return HttpResponseRedirect('/')

#Allows a user to change/edit a review that he submitted previously
def update_review(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            what = request.POST.get('what')
            #Edit review
            if what == "update":    
                id = request.POST.get('id')
                reviewText = request.POST.get('review')
                rating = request.POST.get('rating')
                review = Review.objects.get(id=id)
                review.reviewText = reviewText
                review.rating = rating
                review.save()
                return HttpResponse("success")
            #Delete review
            if what == "delete":
                id = request.POST.get('id')
                review = Review.objects.get(id=id)
                review.delete()
                return HttpResponse("success")                
                                
