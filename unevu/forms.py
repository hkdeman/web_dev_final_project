from django.contrib.auth.models import User
from django import forms

#Form for user accounts
class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your first name'}), required = True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your last name'}), required = True)
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter a username'}), required = True)
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your email address'}), required = True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter a password'}), required = True)

    class Meta: 
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password')
        
        