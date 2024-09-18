from django.shortcuts import render, redirect
from social_media_app.forms import RegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

def home_view(request):
  return render(request, 'home.html')

def about_view(request):
  return render(request, 'about.html')

def registered_view(request):
  return render(request,'registered.html')

@login_required(login_url='/login/')
def feed_view(request):
  return render(request, 'feed.html')

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