from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment
from pages.models import Profile

class Posts(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(username='postuser', password='bigpassword1919!!')
    self.profile = Profile.objects.create(user=self.user, display_name='Post User')
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
    response = self.client.get(reverse('post_detail', kwargs={'id': self.post.id}))
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
    response = self.client.get(reverse('post_detail', kwargs={'id': self.post.id}))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'Test comment')
    
class Like(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(username='likeuser', password='bigpassword098##')
    self.client.login(username='likeuser', password='bigpassword098##')
    self.post = Post.objects.create(author=self.user, content='Like Post')
    
  def test_like_post(self):
    response = self.client.post(reverse('feed'), {'post_id': self.post.id, 'action': 'like'})
    self.assertEqual(response.status_code, 302)  # Should redirect after action
    self.assertEqual(self.post.likes.count(), 1)

  def test_duplicate_likes(self):
    # Test that a user cannot like a post multiple times
    self.client.post(reverse('feed'), {'post_id': self.post.id, 'action': 'like'})
    self.assertEqual(self.post.likes.count(), 1)

    # Try liking the post again
    self.client.post(reverse('feed'), {'post_id': self.post.id, 'action': 'like'})
    self.assertEqual(self.post.likes.count(), 0)  # Should remove the like

  def test_unlike_post(self):
    self.post.likes.add(self.user)
    response = self.client.post(reverse('feed'), {'post_id': self.post.id, 'action': 'like'})
    self.assertEqual(response.status_code, 302)
    self.assertEqual(self.post.likes.count(), 0)

  def test_dislike_then_like_post(self):
    # Test if a user can dislike a post => then like it, ensuring dislikes are removed."""
    self.client.post(reverse('feed'), {'post_id': self.post.id, 'action': 'dislike'})
    self.assertEqual(self.post.dislikes.count(), 1)
    self.assertEqual(self.post.likes.count(), 0)
    self.client.post(reverse('feed'), {'post_id': self.post.id, 'action': 'like'})
    self.assertEqual(self.post.dislikes.count(), 0)
    self.assertEqual(self.post.likes.count(), 1)
    
class Dislike(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(username='dislikeuser', password='bigpassword1234$$')
    self.client.login(username='dislikeuser', password='bigpassword1234$$')
    self.post = Post.objects.create(author=self.user, content='Dislike Post')
    
  def test_dislike_post(self):
    response = self.client.post(reverse('feed'), {'post_id': self.post.id, 'action': 'dislike'})
    self.assertEqual(response.status_code, 302)
    self.assertEqual(self.post.dislikes.count(), 1)
    
  def test_duplicate_dislikes(self):
    # Test that a user cannot dislike a post multiple times
    self.client.post(reverse('feed'), {'post_id': self.post.id, 'action': 'dislike'})
    self.assertEqual(self.post.dislikes.count(), 1)

    # Try disliking the post again
    self.client.post(reverse('feed'), {'post_id': self.post.id, 'action': 'dislike'})
    self.assertEqual(self.post.dislikes.count(), 0)  # Should remove the dislike

    # Now like the post
    self.client.post(reverse('feed'), {'post_id': self.post.id, 'action': 'like'})
    self.assertEqual(self.post.dislikes.count(), 0)
    self.assertEqual(self.post.likes.count(), 1)

  def test_remove_dislike(self):
    self.post.dislikes.add(self.user)
    response = self.client.post(reverse('feed'), {'post_id': self.post.id, 'action': 'dislike'})
    self.assertEqual(response.status_code, 302)
    self.assertEqual(self.post.dislikes.count(), 0)
    
  def test_like_then_dislike_post(self):
    # Test if a user can like a post => then dislike it, ensuring likes are removed
    self.client.post(reverse('feed'), {'post_id': self.post.id, 'action': 'like'})
    self.assertEqual(self.post.likes.count(), 1)
    self.assertEqual(self.post.dislikes.count(), 0)

    # Now dislike the post
    self.client.post(reverse('feed'), {'post_id': self.post.id, 'action': 'dislike'})
    self.assertEqual(self.post.likes.count(), 0)
    self.assertEqual(self.post.dislikes.count(), 1)