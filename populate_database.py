import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','web_dev_final_project.settings')

from tqdm import tqdm
import json
import django
django.setup()

from unevu.models import *

def add_uni(name, location):
	uni = University.objects.get_or_create(name=name, location=location)[0]
	uni.save()
	return uni

def add_school(name, uni):
	school = School.objects.get_or_create(name=name, university=uni)[0]
	school.save()
	return school

def add_teacher(name,school):
	teacher = Teacher.objects.get_or_create(name=name, school=school)[0]
	teacher.save()
	return teacher

def add_course(name, school, url, description=" "):
	course = Course.objects.get_or_create(name=name, school=school, url=url, description=description)[0]
	course.save()
	return course

def set_convener_to_course(course, teacher):
	course.convener = teacher
	add_teacher_to_course(course, teacher)
	

def add_teacher_to_course(course, teacher):
	course.teachers.add(teacher)
	course.save()

def add_user(username, email, first_name, last_name, password = "hunter2"):
	user, created = User.objects.get_or_create(username=username, email=email)
	if not created:
	    user.set_password(password)
	    user.first_name = first_name
	    user.last_name = last_name
	    2
	user_profile = UserProfile.objects.get_or_create(user=user)[0]
	return user_profile

def add_course_review(course, user, review, rating):
	course_review = CourseReview.objects.get_or_create(course=course,username=user,reviewText=review,rating=rating)[0]
	course_review.save()
	return course_review


file = open("assets/glasgow_university_subject_data.json", "r")
glasgow_courses = json.loads(file.read())

file = open("assets/glasgow_university_teacher_data.json", "r")
glasgow_teachers = json.loads(file.read())

file = open("assets/top_50_university_data.json","r")
universities = json.loads(file.read())


for university in tqdm(universities,desc="Adding Universities"):
	add_uni(university, "United Kingdom")

gla = add_uni("University of Glasgow", "Glasgow, Scotland")

for school in glasgow_courses:
	curr_school = add_school(school["title"], gla)
	print("Processing " + school["title"] + " courses")
	for course in tqdm(school.get("subjects", [])):
		add_course(course["title"], curr_school, "https://www.gla.ac.uk"+course["url"], course["description"] )

	print("Processing " + school["title"] + " teachers")
	for teacher in tqdm(glasgow_teachers.get(school.get("title", []), [])):
		add_teacher(teacher["name"], curr_school)
	print()

#Sets test review for Economics 1A
course = Course.objects.get(id = 1)
teacher = Teacher.objects.get(name = "Harless, Dr Patrick")
set_convener_to_course(course,teacher)

test_user = add_user("mrtest", "mrtest@test.com", "Test", "User")
add_course_review(course, test_user, "Very good course. Fandabbydozy!", 4)
