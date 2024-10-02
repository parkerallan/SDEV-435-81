from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment

class Posts(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(username='postuser', password='bigpassword1919!!')
    self.client.login(username='postuser', password='bigpassword1919!!')
    self.post = Post.objects.create(author=self.user, content='This is a test post')
    
  def test_post_creation(self):
    post_count = Post.objects.count()
    self.assertEqual(post_count, 1)
    self.assertEqual(self.post.content, 'This is a test post')

  def test_post_list_view(self):
    response = self.client.get(reverse('feed'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'This is a test post')

  def test_post_detail_view(self):
    response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'This is a test post')

