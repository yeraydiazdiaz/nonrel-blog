"""

    Module to host tests over the blog app.
    Requires the test_aux module for auxiliary functions.

"""

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
        self.assertGreater( len(p.comments), 0)
        self.assertNotEquals( p.comments[0].author, None)

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
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 1)
        
    def test_home_view_with_several_post(self):
        """Test home view in case there several posts in the database.
        
        """
        reset_db()
        for i in xrange(5):
            create_post_with_comments()
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 5)        
                
    def test_post_view_non_existent_permalink(self):
        """Test post view with a non existent permalink.
        
        """
        reset_db()
        c = Client()
        response = c.get('/post/foobar')
        self.assertEqual(response.status_code, 404)    
    
    def test_single_post_view(self):
        """Test post view with a sample post.
        
        """
        reset_db()
        p = create_post_with_comments()
        c = Client()
        response = c.get('/post/%s/%s' % (p.id, p.permalink) )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], 1)