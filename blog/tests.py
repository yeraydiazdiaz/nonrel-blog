"""

    Module to host tests over the blog app.
    Requires the test_aux module for auxiliary functions.

"""

import datetime
from django.test import TestCase, Client
from django.core import management
from blog.models import *
from test_aux import *

class BlogTests(TestCase):
    
    def test_embedded_comments_and_authors(self):
        """Test correctness of post, comment and author embedded lists.
        
        """
        reset_db()
        p = create_post_with_comments()
        p.save()
        p = Post.objects.get(title='Test post')
        self.assertGreater( len(p.comments), 0, 'No comments in post.')
        for c in p.comments:
            self.assertIsNotNone( c.author, 'No author in comment:\n %s.' % c)
            self.assertIsNotNone( c.text, 'No text in comment:\n %s.' % c)

    def test_home_view_with_no_posts(self):
        """Test home view in case there are no posts in the database.
        
        """
        reset_db()
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual( len(response.context['posts']), 0 )

    def test_home_view_with_one_post(self):
        """Test home view in case there is only one post in the database.
        
        """
        reset_db()
        p = create_post_with_comments()
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200, 'HTTP error.')
        self.assertEqual(len(response.context['posts']), 1, 'Expected only one post.')
        
    def test_home_view_with_several_post(self):
        """Test home view in case there several posts in the database.
        
        """
        reset_db()
        for i in xrange(5):
            create_post_with_comments()
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200, 'HTTP error.')
        self.assertEqual(len(response.context['posts']), 5, 'Unexpected number of posts.')   
                
    def test_post_view_non_existent_permalink(self):
        """Test post view with a non existent permalink.
        
        """
        reset_db()
        c = Client()
        response = c.get('/post/foobar')
        self.assertEqual(response.status_code, 404, 'Expected 404.')    
    
    def test_single_post_view(self):
        """Test post view with a sample post.
        
        """
        reset_db()
        p = create_post_with_comments()
        c = Client()
        response = c.get('/post/%s/%s' % (p.id, p.permalink) )
        self.assertEqual(response.status_code, 200, 'HTTP error.')
        self.assertIsNotNone(response.context['post'], 'No post returned.')
        
    def test_invalid_form_submit_produces_errors(self):
        """Test showing errors on invalid comment form submission.
        
        """
        reset_db()
        p = create_post_with_comments()
        c = Client()
        response = c.get('/post/%s/%s' % (p.id, p.permalink) )
        self.assertEqual(response.status_code, 200, 'HTTP error.')
        for f in response.context['forms']:
            self.assertIsNotNone(f.errors, 'Expected error, got None on form %s.' % f)
        
    def test_valid_form_submit_creates_new_comment(self):
        """Test showing errors on invalid comment form submission.
        
        """
        reset_db()
        p = create_post_with_comments()
        original_num_comments = len( p.comments )
        c = Client()
        response = c.post('/post/%s/%s' % (p.id, p.permalink), {
                                'name': 'John',
                                'email': 'john@example.org',
                                'text': 'Test comment'
                            }
                          )
        self.assertEqual(response.status_code, 200, 'HTTP error.')
        for f in response.context['forms']:
            self.assertIsNotNone(f.errors, 'Unexpected error on form %s.' % f)
        
        p = Post.objects.get(title='Test post')
        self.assertLessEqual( original_num_comments, len( p.comments ) )
        
    def test_tag_view(self):
        """Test tag view through url and correctness of content.
        
        """
        reset_db()
        for i in range(5):
            p = create_post('Test post %s' % i)
            if i < 3:
                p.tags = [ tags[0] ]
            else:
                p.tags = [ tags[1] ]
            p.save()
        
        c = Client()
        response = c.get('/tag/%s' % tags[0])    
        self.assertEqual(response.status_code, 200, 'HTTP error.')
        self.assertEqual(len( response.context['posts'] ), 3, 'Incorrect number of posts returned.')

    def test_tag_view_non_existent_tag(self):
        """Test tag view through url and correctness of content.
        
        """
        reset_db()
        c = Client()
        response = c.get('/tag/foo')    
        self.assertEqual(response.status_code, 200, 'HTTP error.')
        self.assertEqual(len( response.context['posts'] ), 0, 'Incorrect number of posts returned.')

    def test_login_view(self):
        """Test response from login view.

        """
        reset_db()
        c = Client()
        response = c.post('/login')    
        self.assertEqual(response.status_code, 200, 'HTTP error.')
        self.assertIsNotNone(response.context['form'], 'No login form in login page.')

    def test_incorrect_login(self):
        """Test response from an incorrect login.

        """
        reset_db()
        c = Client()
        response = c.post('/login', { 'username': 'foo', 'password':'bar' })   
        self.assertEqual(response.status_code, 200, 'HTTP error.')
        self.assertIsNotNone(response.context['login_failed'], 'Unexpected non errors on login form.')

    def test_correct_login(self):
        """Test response from an incorrect login.

        """
        from django.contrib.auth.models import User
        reset_db()
        create_user()
        c = Client()
        response = c.post('/login', { 'username': 'John', 'password':'foobar' })
        self.assertNotEqual(response.status_code, 404, 'HTTP error.')
        u = User.objects.get( username='John' )
        self.assertEqual(c.session['_auth_user_id'], u.pk, 'Login unsuccessful.')

    def test_correct_logout(self):
        """Test logout sequence.

        """
        from django.contrib.auth.models import User
        reset_db()
        u = create_user()
        c = Client()
        response = c.post('/login', { 'username': 'John', 'password':'foobar' })
        self.assertNotEqual(response.status_code, 404, 'HTTP error on login.')
        response = c.get('/logout')
        self.assertNotEqual(response.status_code, 404, 'HTTP error on logout.')
        u = User.objects.get( username=u.username )
        self.assertEquals(c.session.get( '_auth_user_id', None ), None, 'Logout unsuccessful.')

    def test_register_view(self):
        """Test registration view.

        """
        c = Client()
        response = c.post('/register', { 'username': 'John', 'password':'foobar' })
        self.assertNotEqual(response.status_code, 404, 'HTTP error on register.')

    def test_register_user(self):
        """Test registration sequence.

        """
        from django.contrib.auth.models import User
        reset_db()
        c = Client()
        response = c.post('/register', { 'username': 'John', 'password1':'foobar', 'password2':'foobar' })
        self.assertNotEqual(response.status_code, 404, 'HTTP error on register.')
        u = User.objects.get(username='John')
        self.assertIsNotNone(u, 'User not created.')

    def test_mismatch_password_register_failed(self):
        """Test registration failure.

        """
        from django.contrib.auth.models import User
        reset_db()
        c = Client()
        response = c.post('/register', { 'username': 'John', 'password1':'foo', 'password2':'bar' })
        self.assertNotEqual(response.status_code, 404, 'HTTP error on register.')
        self.assertEquals(User.objects.all().count(), 0, 'Unexpected user in database.')

    def test_create_post_view_redirects_anonymous_users(self):
        """Test create post view.

        """
        c = Client()
        response = c.get('/create_post')
        self.assertEqual(response.status_code, 302, 'Expected HTTP redirection on create post view.')

    def test_create_post_view(self):
        """Test create post view.

        """
        from django.contrib.auth.models import User
        u = User.objects.create_user('John', 'johndoe@example.org', 'foobar')
        u.save()
        c = Client()
        c.post('/login', { 'username': 'John', 'password':'foobar' })
        response = c.get('/create_post')
        self.assertEqual(response.status_code, 200, 'HTTP error on create post view.')

    def test_create_post_correctly(self):
        """Test create post view.

        """
        reset_db()
        response, c = create_and_login_user()
        response = c.post('/create_post', { 'title': 'test_create_post_correctly', 'text': 'This is a test post' } )
        self.assertEqual(response.status_code, 302, 'Expected HTTP redirection on create post view.')
        self.assertGreater(Post.objects.all().count(), 0, 'Expected 1 post in database, got 0.')