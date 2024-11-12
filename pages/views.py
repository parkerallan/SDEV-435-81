# Description: This file contains the views for the pages app.
# The views are used to render the templates for the pages app.
# The views also handle the logic for user registration, login, and profile management.
# Some views only render the templates, while others handle form submissions and user authentication.

from django.shortcuts import render, redirect
from social_media_app.forms import RegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from social_media_app.forms import ProfileUpdateForm, UserUpdateForm
from .models import Profile
from posts.models import Activity
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

def home_view(request):                                             # Render home page
  return render(request, 'home.html')

def login_view(request):                                            # Login logic, redirecting, and rendering
  if request.method == 'POST':                                      
      username = request.POST.get('username')                       # Get username from form
      password = request.POST.get('password')                       # Get password from form 
      user = authenticate(username=username, password=password)     # Authenticate user
      if user:                                                      # If user is authenticated
          login(request, user)                                      # Log user in
          return redirect('feed')                                   # Redirect user to the feed as the landing page
  if request.user.is_authenticated:                                 # If user is already authenticated when trying to access login page
      return redirect('feed')                                       # Redirect user to the feed
  else:                                                             # If user is not authenticated
      return render(request, 'login.html')                          # Render login page instead

def about_view(request):                                            # Render about page
  return render(request, 'about.html')

def registered_view(request):                                       # Render registration success page
  return render(request,'registered.html')

def redirect_to_website(request):                                   # Redirect users to my website :)
  return redirect('https://www.parkerdev.net/#contact')

def register_view(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)                           # Create a form instance and populate it with data from the request (binding)
    if form.is_valid():                                             # Check if the form is valid
      user = form.save()                                            # Save the form data to the database
      
      # We're adding users to this group to manage them in the admin portal
      group, created = Group.objects.get_or_create(name='Members')  # Get or create a group called 'Members'
      user.groups.add(group)                                        # Add the user to the 'Members' group

      return redirect('/registered/')
  else:
    form = RegistrationForm()                                       # Create an empty form
    
  return render(request, 'registration/register.html', {'form': form}) # Render the registration form


@login_required(login_url='/login/')                                # Require user to be logged in to access this view
def my_profile(request):
  try:                                                              # Try to get the profile for a user
      profile = request.user.profile
  except Profile.DoesNotExist:                                      # If the profile does not exist
      profile = Profile.objects.create(user=request.user)           # Create a new profile for the user, this should be done for new users and is a fallback for premigration users

  if request.method == 'POST':
      profile_form = ProfileUpdateForm(request.POST, instance=profile) # Create a form instance and populate it with data from the request
      
      if profile_form.is_valid():                                   # Check if the form is valid
          profile_form.save()                                       # Save the form data to the database
          return redirect('myprofile')                              # Redirect user to the profile page
  else:
      profile_form = ProfileUpdateForm(instance=profile)            # Create a form instance and populate it with data from the profile

  activities = Activity.objects.filter(user=request.user).order_by('-created_at')[:5] # Get the latest 5 activities for the user
  
  context = {                                                       # Context to pass to the template
      'profile_form': profile_form,
      'activities': activities
  }
  return render(request, 'my_profile.html', context)

@login_required(login_url='/login/')
@require_http_methods(["GET"])                                      # Only allow GET requests for this view
def user_profile(request, id):
    profile = get_object_or_404(Profile, id=id)                     # Get the profile by its ID value
    user = profile.user                                             # Get the user associated with the profile
    activities = Activity.objects.filter(user=user).order_by('-created_at')[:5] # Get the latest 5 activities for the user
    
    context = {                                                     # Context to pass to the template
        'user': user,
        'profile': profile,
        'activities': activities
    }
    return render(request, 'user_profile.html', context)