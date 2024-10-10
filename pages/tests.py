from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile

class Status(TestCase):
  def test_home_page_access(self):
    response = self.client.get(reverse('home'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'home.html')
    
  def test_about_page_access(self):
    response = self.client.get(reverse('about'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'about.html')
    
  def test_contact_page_access(self):
    response = self.client.get(reverse('contact'))
    self.assertEqual(response.status_code, 302) # Indicates that the request is being redirected
    self.assertEqual(response['Location'], 'https://www.parkerdev.net/#contact')
    
class Login(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'password1234$'
        User.objects.create_user(username=self.username, password=self.password)

    def test_login_page_access(self):
      response = self.client.get(reverse('login'))
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'registration/login.html')
      
    def test_login_valid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertRedirects(response, reverse('feed'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
    def test_login_invalid_credentials(self):
      response = self.client.post(reverse('login'), {
          'username': 'wronguser',
          'password': 'wrongpassword1234$'
      })
      self.assertEqual(response.status_code, 200)
      self.assertContains(response, "Please enter a correct username and password.")
      self.assertFalse(response.wsgi_request.user.is_authenticated)
      
    def test_logout_functionality(self):
      self.client.login(username=self.username, password=self.password)
      response = self.client.get(reverse('logout'))
      self.assertRedirects(response, reverse('login'))  # Redirect to login page after logging out
      self.assertFalse(response.wsgi_request.user.is_authenticated)
      
class Register(TestCase):
  def test_register_page_access(self):
    response = self.client.get(reverse('register'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'registration/register.html')
    
  def test_registering_valid_user(self):
    response = self.client.post(reverse('register'), {
        'username': 'validuser',
        'email': 'validuser@example.com',
        'password1': 'password1234$',
        'password2': 'password1234$'
    })
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, reverse('registered'))
    user = User.objects.get(username='validuser')
    self.assertEqual(user.email, 'validuser@example.com')
  
  def test_register_user_with_mismatched_passwords(self):
        response = self.client.post(reverse('register'), {
            'username': 'mismatchuser',
            'email': 'mismatchuser@example.com',
            'password1': 'password123%',
            'password2': 'wrongpassword89'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', "The two password fields didn’t match.")
        
  def test_register_user_with_missing_email(self):
        response = self.client.post(reverse('register'), {
            'username': 'noemailuser',
            'password1': 'strongpassword123&',
            'password2': 'strongpassword123&'
        })

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', "This field is required.")

  def test_register_user_with_existing_username(self):
      # Create a user to simulate username conflict
      User.objects.create_user(username='sameuser', email='sameuser1@example.com', password='password123$')

      # Try to register another user with the same username
      response = self.client.post(reverse('register'), {
          'username': 'sameuser',
          'email': 'sameuser2@example.com',
          'password1': 'strongpassword123',
          'password2': 'strongpassword123'
      })

      self.assertEqual(response.status_code, 200)
      self.assertFormError(response, 'form', 'username', "A user with that username already exists.")

  def test_register_user_with_short_password(self):
      response = self.client.post(reverse('register'), {
          'username': 'passshortuser',
          'email': 'passshortuser@example.com',
          'password1': 'short',
          'password2': 'short'
      })

      self.assertEqual(response.status_code, 200)
      self.assertFormError(response, 'form', 'password2', "This password is too short. It must contain at least 8 characters.")

class UserProfiles(TestCase):
  def setUp(self):
      # Create two users -> one for the authenticated user and another to test the public profile view.
      self.user1 = User.objects.create_user(username='testuser1', password='password123', email='user1@example.com')
      self.user2 = User.objects.create_user(username='testuser2', password='password123', email='user2@example.com')

      self.profile1 = Profile.objects.create(user=self.user1, display_name="User One", bio="User One Bio", social_links="https://twitter.com/user1")
      self.profile2 = Profile.objects.create(user=self.user2, display_name="User Two", bio="User Two Bio", social_links="https://twitter.com/user2")

      self.client.login(username='testuser1', password='password123')

  def test_my_profile_view_accessible(self):
      response = self.client.get(reverse('myprofile'))
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'my_profile.html')

  def test_my_profile_initial_data(self):
      response = self.client.get(reverse('myprofile'))
      self.assertContains(response, 'User One')
      self.assertContains(response, 'User One Bio')
      self.assertContains(response, 'https://twitter.com/user1')

  def test_my_profile_update(self):
      """Test that a user can update their profile information."""
      response = self.client.post(reverse('myprofile'), {
          'display_name': 'Updated User One',
          'bio': 'Updated bio for User One',
          'social_links': 'https://linkedin.com/in/user1',
      })
      self.assertEqual(response.status_code, 302)  # redirect after update

      self.profile1.refresh_from_db()
      self.assertEqual(self.profile1.display_name, 'Updated User One')
      self.assertEqual(self.profile1.bio, 'Updated bio for User One')
      self.assertEqual(self.profile1.social_links, 'https://linkedin.com/in/user1')

  def test_my_profile_empty_display_name(self):
      response = self.client.post(reverse('myprofile'), {
          'display_name': '',
          'bio': 'Bio with empty display name',
          'social_links': 'https://twitter.com/user1',
      })
      self.assertEqual(response.status_code, 302)

      self.profile1.refresh_from_db()
      self.assertEqual(self.profile1.display_name, '')  # Display name can be blank
      self.assertEqual(self.profile1.bio, 'Bio with empty display name')

  def test_my_profile_invalid_url(self):
      response = self.client.post(reverse('myprofile'), {
          'display_name': 'User One',
          'bio': 'Bio for User One',
          'social_links': 'invalid-url',
      })
      self.assertEqual(response.status_code, 200)
      self.assertFormError(response, 'profile_form', 'social_links', 'Enter a valid URL.')

  def test_user_profile_view_accessible(self):
      response = self.client.get(reverse('userprofile', kwargs={'user_id': self.user2.id}))
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'user_profile.html')

  def test_user_profile_content(self):
      response = self.client.get(reverse('userprofile', kwargs={'user_id': self.user2.id}))
      self.assertContains(response, 'User Two')
      self.assertContains(response, 'User Two Bio')
      self.assertContains(response, 'https://twitter.com/user2')

  def test_user_profile_read_only(self):
      # Try posting to the public profile URL of another user
      response = self.client.post(reverse('userprofile', kwargs={'user_id': self.user2.id}), {
          'display_name': 'Should Not Change',
          'bio': 'This should not work',
          'social_links': 'https://linkedin.com/in/user2',
      })
      self.assertEqual(response.status_code, 405)  # 405 - POST Method Not Allowed

      # Ensure that the other user's profile was not changed
      self.profile2.refresh_from_db()
      self.assertEqual(self.profile2.display_name, 'User Two')
      self.assertEqual(self.profile2.bio, 'User Two Bio')
      self.assertEqual(self.profile2.social_links, 'https://twitter.com/user2')