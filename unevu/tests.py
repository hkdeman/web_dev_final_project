from django.test import TestCase
from django.contrib.staticfiles import finders
from django.conf import settings
from unevu.models import *
import unevu.test_utils as test_utils

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
        user = test_utils.create_user()

        # Check there is only the saved user
        self.assertEqual(1, User.objects.count(), "Number of Profiles must be 1")

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
        test_utils.create_user()
        
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
