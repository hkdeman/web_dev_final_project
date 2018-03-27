from django.db import models
from django.contrib.auth.models import User

#Model for user profile
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	def __str__(self):
		return self.user.username

#Model for reviews stored
class Review(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewText = models.CharField(max_length=300)
    rating = models.IntegerField()
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return "Review: "+self.reviewText + "\n Ratings: "+str(self.rating)+"\n Likes: "+str(self.likes)

#Model for the universities
class University(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=120)
    description = models.CharField(default="",max_length=1000)
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)
    avgRating = models.FloatField(default=0)
    noOfRatings = models.FloatField(default=0)

    def __str__(self):
        return self.name+" "+str(self.lat)+" "+str(self.lng)+" "+self.description

#Model for the schools in each university
class School(models.Model):
    name = models.CharField(max_length=60)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

#Model for a teacher
class Teacher(models.Model):
    name = models.CharField(max_length=30)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    email = models.EmailField(null=True)
    mobile = models.CharField(max_length=14, null=True)
    imageUrl = models.URLField(null=True)
    avgRating= models.FloatField(default=0)
    noOfRatings = models.FloatField(default=0)
    def __str__(self):
        return self.name


#Model for a course
class Course(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=60)
    convener = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="course_convener", null=True)
    teachers = models.ManyToManyField(Teacher)
    description = models.CharField(max_length=1000, default=" ")
    url = models.URLField(blank=True)
    avgRating= models.FloatField(default=0)
    noOfRatings = models.FloatField(default=0)
    def __str__(self):
        return self.name

#Models for different reviews (university, teacher, course)
class CourseReview(Review):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class UniReview(Review):
    university = models.ForeignKey(University, on_delete=models.CASCADE)

class TeacherReview(Review):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    
#Model for like function
class Like(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

#Model for adding a teacher to a course
class Request(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)    
    def __str__(self):
        return str(self.username) + " wants to add "+self.teacher.name+" as convener of "+self.course.name+" of "+self.course.school.university.name