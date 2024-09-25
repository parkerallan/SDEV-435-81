from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

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