from django.test import TestCase
from django.contrib.staticfiles import finders
from django.conf import settings
from unevu.models import *
import unevu.utils as util

import os

class GeneralTestCases(TestCase):
    def test_static_files(self):
        # Check if static media is used properly 
        result = finders.find(settings.STATICFILES_DIRS[0] + '/images/unevu-logo.png')
        self.assertIsNotNone(result)
        
    def test_base_template(self):
        # Check that base.html is present
        path_to_base = settings.TEMPLATE_DIR + '/unevu/base.html'
        self.assertTrue(os.path.isfile(path_to_base))
        
    def test_logo_exists(self):
        # Check if logo exists
        path_to_logo = settings.STATICFILES_DIRS[0] + '/images/unevu-logo.png'
        self.assertTrue(os.path.isfile(path_to_logo))
        
class ModelTestCases(TestCase):
    def test_user_profile_model(self):
        # Create a user
        user = util.add_user("mrtest1", "mrtest1@test.com", "Test1", "User")

        # Check there is only the saved user
        self.assertEqual(1, User.objects.count(), "Number of Profiles must be 1")

    def test_university_model(self):
        uni = util.add_uni("Test Uni", "Test Location", "Test Description", 55.8721211,-4.2882005)
        unis_in_db = University.objects.all()
        self.assertEqual(1, unis_in_db.count())
        uni_in_db = unis_in_db[0]
        
        #Check if university is saved correctly
        self.assertEqual(uni, uni_in_db)
        self.assertEqual(uni_in_db.name, "Test Uni")
        self.assertEqual(uni_in_db.location, "Test Location")
        self.assertEqual(uni_in_db.description, "Test Description")
        self.assertEqual(uni_in_db.noOfRatings, 0)
        self.assertEqual(uni_in_db.avgRating, 0)
        self.assertEqual(uni_in_db.lat, 55.8721211)
        self.assertEqual(uni_in_db.lng, -4.2882005)

    def test_uni_review(self):
        user = util.add_user("mrtest1", "mrtest1@test.com", "Test1", "User")
        user2 = util.add_user("mrtest2", "mrtest2@test.com", "Test2", "User")
        uni = util.add_uni("Test Uni", "Test Location", "Test Description", 55.8721211,-4.2882005)
        
        #Check both reviews save
        util.add_uni_review(uni, user, "Review test", 3)
        uni_reviews = UniReview.objects.all();
        self.assertEqual(1, uni_reviews.count())
        util.add_uni_review(uni, user2, "Review test 2", 4)
        uni_reviews = UniReview.objects.all();
        self.assertEqual(2, uni_reviews.count())

        first_review = uni_reviews[0]
        self.assertEqual(first_review.university, uni)
        self.assertEqual(first_review.reviewText, "Review test")

        #Check if ratings are calculated properly
        uni_in_db = University.objects.all()[0]
        self.assertEqual(uni_in_db.avgRating, 3.5)
        self.assertEqual(uni_in_db.noOfRatings, 2)

    def test_school_model(self):
        uni = util.add_uni("Test Uni", "Test Location", "Test Description", 55.8721211,-4.2882005)
        school = util.add_school("School name", uni)
        schools = School.objects.all()
        
        #Check if school is saved correctly
        self.assertEqual(1, schools.count())
        self.assertEqual(schools[0].name, "School name")
        self.assertEqual(schools[0].university, uni)

    def test_course_model(self):
        uni = util.add_uni("Test Uni", "Test Location", "Test Description", 55.8721211,-4.2882005)
        school = util.add_school("School name", uni)
        util.add_course("Course title", school, "https://www.gla.ac.uk" , "Description" )
        courses = Course.objects.all()
        course_in_db = courses[0]
        
        #Check if course is saved correctly
        self.assertEqual(1, courses.count())
        self.assertEqual(course_in_db.school, school)
        self.assertEqual(course_in_db.url, "https://www.gla.ac.uk")
        self.assertEqual(course_in_db.name, "Course title")
        self.assertEqual(course_in_db.description, "Description")
        self.assertEqual(course_in_db.avgRating, 0)
        self.assertEqual(course_in_db.noOfRatings, 0)


    def test_course_review(self):
        user = util.add_user("mrtest1", "mrtest1@test.com", "Test1", "User")
        user2 = util.add_user("mrtest2", "mrtest2@test.com", "Test2", "User")
        uni = util.add_uni("Test Uni", "Test Location", "Test Description", 55.8721211,-4.2882005)
        school = util.add_school("School name", uni)
        course = util.add_course("Course title", school, "https://www.gla.ac.uk" , "Description" )
        
        #Check both reviews save
        util.add_course_review(course, user, "Review test", 3)
        course_reviews = CourseReview.objects.all();
        self.assertEqual(1, course_reviews.count())
        util.add_course_review(course, user2, "Review test 2", 4)
        course_reviews = CourseReview.objects.all();
        self.assertEqual(2, course_reviews.count())

        first_review = course_reviews[0]
        self.assertEqual(first_review.course, course)
        self.assertEqual(first_review.reviewText, "Review test")

        #Check if ratings are calculated properly
        course_in_db = Course.objects.all()[0]
        self.assertEqual(course_in_db.avgRating, 3.5)
        self.assertEqual(course_in_db.noOfRatings, 2)


    def test_teacher_model(self):
        uni = util.add_uni("Test Uni", "Test Location", "Test Description", 55.8721211,-4.2882005)
        school = util.add_school("School name", uni)
        teacher = util.add_teacher("Name", school, "email@website.com", "01234567890", "https://website.com/image.jpeg")
        teachers = Teacher.objects.all()
        teacher_in_db = teachers[0]
        
        #Check if the teacher is saved 
        self.assertEqual(1, teachers.count())
        self.assertEqual(teacher_in_db.school, school)
        
        #Check if info are correct
        self.assertEqual(teacher_in_db.email, "email@website.com")
        self.assertEqual(teacher_in_db.name, "Name")
        self.assertEqual(teacher_in_db.mobile, "01234567890")
        self.assertEqual(teacher_in_db.imageUrl, "https://website.com/image.jpeg")
        self.assertEqual(teacher_in_db.avgRating, 0)
        self.assertEqual(teacher_in_db.noOfRatings, 0)

class ViewTests(TestCase):
    def test_registration_form_is_displayed_correctly(self):
        #Access registration page
        try:
            response = self.client.get(reverse('register'))
        except:
            try:
                response = self.client.get(reverse('unevu:register'))
            except:
                return False

        # Check if form is rendered correctly
        self.assertIn('<h1>Register</h1>'.lower(), response.content.decode('ascii').lower())

        # Check form in response context is instance of UserForm
        self.assertTrue(isinstance(response.context['form'], UserForm))

        form = UserForm()

        # Check form is displayed correctly
        self.assertEquals(response.context['form'].as_p(), form.as_p())

        # Check submit button
        self.assertIn('type="submit"', response.content.decode('ascii'))
        self.assertIn('name="submit"', response.content.decode('ascii'))
        self.assertIn('value="Register"', response.content.decode('ascii'))

    def test_login_form_is_displayed_correctly(self):
        #Access login page
        try:
            response = self.client.get(reverse('login'))
        except:
            try:
                response = self.client.get(reverse('unevu:login'))
            except:
                return False

        #Check form display
        #Header
        self.assertIn('<h1>Login</h1>'.lower(), response.content.decode('ascii').lower())

        #Username label and input text
        self.assertIn('Username:', response.content.decode('ascii'))
        self.assertIn('input type="text"', response.content.decode('ascii'))
        self.assertIn('name="username"', response.content.decode('ascii'))
        self.assertIn('size="50"', response.content.decode('ascii'))

        #Password label and input text
        self.assertIn('Password:', response.content.decode('ascii'))
        self.assertIn('input type="password"', response.content.decode('ascii'))
        self.assertIn('name="password"', response.content.decode('ascii'))
        self.assertIn('value=""', response.content.decode('ascii'))
        self.assertIn('size="50"', response.content.decode('ascii'))

        #Submit button
        self.assertIn('input type="submit"', response.content.decode('ascii'))
        self.assertIn('value="login"', response.content.decode('ascii'))

    def test_login_provides_error_message(self):
        # Access login page
        try:
            response = self.client.post(reverse('login'), {'username': 'wronguser', 'password': 'wrongpass'})
        except:
            try:
                response = self.client.post(reverse('unevu:login'), {'username': 'wronguser', 'password': 'wrongpass'})
            except:
                return False

        print(response.content.decode('ascii'))
        try:
            self.assertIn('wronguser', response.content.decode('ascii'))
        except:
            self.assertIn('Invalid login details supplied.', response.content.decode('ascii'))

    def test_login_redirects_home(self):
        # Create a user
        util.add_user("mrtest1", "mrtest1@test.com", "Test1", "User")
        
        # Access login page via POST with user data
        try:
            response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'test1234'})
        except:
            try:
                response = self.client.post(reverse('unevu:login'), {'username': 'testuser', 'password': 'test1234'})
            except:
                return False

        # Check it redirects to home page
        self.assertRedirects(response, reverse('/'))
