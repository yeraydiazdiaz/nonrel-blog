"""

    RESTful API specific tests.

"""

import json
from django.test import TestCase
from blog.models import *
from blog.test_aux import *
from rest_framework import status

class BlogAPITests(TestCase):

    def test_posts_returns_empty_on_empty_db(self):
        """
        Test posts endpoint with an empty database.
        """
        reset_db()
        c = Client()
        response = c.get('/api/posts')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200.')
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), 0, 'Expected 0 results')

    def test_posts_returns_one_post(self):
        """
        Test posts endpoint with one object in the database.
        """
        reset_db()
        p = create_post()
        c = Client()
        response = c.get('/api/posts')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200.')
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), 1, 'Expected 1 result')

    def test_posts_returns_several_posts(self):
        """
        Test posts endpoint with several objects in the database.
        """
        reset_db()
        p = create_post()
        p = create_post()
        c = Client()
        response = c.get('/api/posts')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200.')
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), 2, 'Expected 1 result')

    def test_post_returns_404_on_empty_db(self):
        """
        Test post endpoint with an empty database.
        """
        reset_db()
        c = Client()
        response = c.get('/api/post/1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, 'Expected HTTP 404.')

    def test_post_with_valid_id_returns_one_post(self):
        """
        Test post endpoint returns the correct result on a valid ID.
        """
        reset_db()
        p = create_post()
        c = Client()
        response = c.get('/api/posts/%s' % p.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200.')
        content = json.loads(response.content)
        self.assertEquals(content['id'], p.id, 'Expected IDs of posts to match.')

    def test_tag_returns_empty_on_empty_db(self):
        """
        Test posts/tag endpoint with an empty database.
        """
        reset_db()
        c = Client()
        response = c.get('/api/posts/tag/foo')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200.')
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), 0, 'Expected 0 results')

    def test_tag_returns_one_post(self):
        """
        Test posts/tag endpoint with an one post.
        """
        reset_db()
        p = create_post(tags=['test-tag'])
        c = Client()
        response = c.get('/api/posts/tag/%s' % p.tags[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200.')
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), 1, 'Expected 1 result')

    def test_tag_returns_several_posts(self):
        """
        Test posts/tag endpoint with several objects in the database.
        """
        reset_db()
        p = create_post(tags=['test-tag'])
        p = create_post(tags=['test-tag'])
        c = Client()
        response = c.get('/api/posts/tag/%s' % p.tags[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200.')
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), 2, 'Expected 1 result')
