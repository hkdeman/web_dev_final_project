from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	def __str__(self):
		return self.user.username

class Review(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewText = models.CharField(max_length=300)
    rating = models.IntegerField()
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return "Review: "+self.reviewText + "\n Ratings: "+str(self.rating)+"\n Likes: "+str(self.likes)

class Comment(models.Model):
    REVIEW_TYPES = (('U','University'),('C','Course'),('T','Teacher'))
    
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewType = models.CharField(max_length=1, choices = REVIEW_TYPES)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

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

class School(models.Model):
    name = models.CharField(max_length=60)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

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

class CourseReview(Review):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class UniReview(Review):
    university = models.ForeignKey(University, on_delete=models.CASCADE)

class TeacherReview(Review):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

class Like(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)