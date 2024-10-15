from django.shortcuts import render, redirect
from social_media_app.forms import RegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from social_media_app.forms import ProfileUpdateForm, UserUpdateForm
from pages.models import Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

def home_view(request):
  return render(request, 'home.html')

def login_view(request):
  if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      user = authenticate(username=username, password=password)
      if user:
          login(request, user)
          return redirect('feed')
  if request.user.is_authenticated:
      return redirect('feed')
  else:
      return render(request, 'login.html')

def about_view(request):
  return render(request, 'about.html')

def registered_view(request):
  return render(request,'registered.html')

def redirect_to_website(request):
  return redirect('https://www.parkerdev.net/#contact')

def register_view(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      user = form.save()
      
      group, created = Group.objects.get_or_create(name='Members')
      user.groups.add(group)

      return redirect('/registered/')
  else:
    form = RegistrationForm()
    
  return render(request, 'registration/register.html', {'form': form})


@login_required(login_url='/login/')
def my_profile(request):
  # Ensure the user has a profile if its a pre-migration account
  try:
      profile = request.user.profile
  except Profile.DoesNotExist:
      profile = Profile.objects.create(user=request.user)

  if request.method == 'POST':
      profile_form = ProfileUpdateForm(request.POST, instance=profile)
      
      if profile_form.is_valid():
          profile_form.save()
          return redirect('myprofile')
  else:
      profile_form = ProfileUpdateForm(instance=profile)

  context = {
      'profile_form': profile_form
  }
  return render(request, 'my_profile.html', context)

@login_required(login_url='/login/')
@require_http_methods(["GET"])  # Only GET requests
def user_profile(request, id):
    # Fetch the profile by its UUID
    profile = get_object_or_404(Profile, id=id)
    user = profile.user  # Access the related user from the profile
    
    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'user_profile.html', context)