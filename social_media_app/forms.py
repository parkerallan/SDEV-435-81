# Description: This file contains the forms for the social media app.
# The forms are used to create the registration form, user update form, and profile update form.
# The forms are created using the Django forms module.
# The forms are used to create the HTML forms that are displayed to the user.
# The forms are used to collect user input and send the data to the server.

from django import forms
from django.contrib.auth.forms import UserCreationForm # Import the UserCreationForm from the Django auth module
from django.contrib.auth.models import User # Import the User model from the Django auth module
from pages.models import Profile

class RegistrationForm(UserCreationForm): # Create a RegistrationForm class that inherits from the UserCreationForm class
  email = forms.EmailField(required=True) # Add an email field to the form
  
  class Meta:
    model = User # Set the model attribute to the User
    fields = ['username', 'email', 'password1', 'password2'] # Set the fields attribute to the fields that we want to display in the form
    
class UserUpdateForm(forms.ModelForm): # Create a UserUpdateForm class that inherits from the ModelForm class
  class Meta:
      model = User
      fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
  class Meta:
      model = Profile
      fields = ['display_name', 'bio', 'social_links']