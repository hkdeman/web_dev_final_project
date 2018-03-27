from unevu.models import *

def add_uni(name, location,desc="",lat=0.0,lng=0.0):
	uni = University.objects.get_or_create(name=name, location=location,description=desc,lat=lat,lng=lng)[0]
	uni.save()
	return uni

def add_school(name, uni):
	school = School.objects.get_or_create(name=name, university=uni)[0]
	school.save()
	return school

def add_teacher(name,school,email,mobile,imageUrl):
	teacher = Teacher.objects.get_or_create(name=name, school=school, email=email, mobile=mobile, imageUrl=imageUrl)[0]
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
	user, created = User.objects.get_or_create(username=username, email=email,first_name=first_name,last_name=last_name)
	if not created:
	    user.set_password(password)
	    user.first_name = first_name
	    user.last_name = last_name
	return user

def add_course_review(course, user, review, rating):
	course_review = CourseReview.objects.get_or_create(course=course,username=user,reviewText=review,rating=rating)[0]
	course_review.save()
	course.avgRating  = (course.avgRating * course.noOfRatings + rating)/(course.noOfRatings+1)
	course.noOfRatings = course.noOfRatings+1
	course.save()
	return course_review

def add_uni_review(university, user, review, rating):
	uni_review = UniReview.objects.get_or_create(university=university,username=user,reviewText=review,rating=rating)[0]
	uni_review.save()
	university.avgRating  = (university.avgRating * university.noOfRatings + rating)/(university.noOfRatings+1)
	university.noOfRatings = university.noOfRatings+1
	university.save()
	return uni_review