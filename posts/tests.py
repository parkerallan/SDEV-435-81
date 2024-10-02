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

class Comments(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(username='commentsuser', password='bigpassword345**')
    self.client.login(username='commentsuser', password='bigpassword345**')
    self.post = Post.objects.create(author=self.user, content='Comment Post')
    
  def test_add_comment_to_post(self):
    response = self.client.post(reverse('feed'), {'post_id': self.post.id, 'content': 'This is a comment'})
    self.assertEqual(response.status_code, 302)  # Should redirect after comment
    comment_count = Comment.objects.count()
    self.assertEqual(comment_count, 1)
    self.assertEqual(self.post.comments.first().content, 'This is a comment')

  def test_add_empty_comment(self):
    response = self.client.post(reverse('feed'), {'post_id': self.post.id, 'content': ''})
    self.assertEqual(response.status_code, 302)  # Should redirect with an error message
    comment_count = Comment.objects.count()
    self.assertEqual(comment_count, 0)

  def test_view_post_with_comments(self):
    Comment.objects.create(post=self.post, author=self.user, content='Test comment')
    response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'Test comment')