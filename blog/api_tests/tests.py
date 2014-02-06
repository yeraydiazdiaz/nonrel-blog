"""

    RESTful API specific tests.

"""

import json
from rest_framework.test import APITestCase
from blog.models import *
from blog.test_aux import *
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient

class BlogAPITests(APITestCase):

    def test_posts_returns_empty_on_empty_db(self):
        """
        Test posts endpoint with an empty database.
        """
        reset_db()
        c = APIClient()
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
        c = APIClient()
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
        c = APIClient()
        response = c.get('/api/posts')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200.')
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), 2, 'Expected 1 result')

    def test_post_returns_404_on_empty_db(self):
        """
        Test post endpoint with an empty database.
        """
        reset_db()
        c = APIClient()
        response = c.get('/api/post/1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, 'Expected HTTP 404.')

    def test_post_with_valid_id_returns_one_post(self):
        """
        Test post endpoint returns the correct result on a valid ID.
        """
        reset_db()
        p = create_post()
        c = APIClient()
        response = c.get('/api/posts/%s' % p.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200.')
        content = json.loads(response.content)
        self.assertEquals(content['id'], p.id, 'Expected IDs of posts to match.')

    def test_tag_returns_empty_on_empty_db(self):
        """
        Test posts/tag endpoint with an empty database.
        """
        reset_db()
        c = APIClient()
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
        c = APIClient()
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
        c = APIClient()
        response = c.get('/api/posts/tag/%s' % p.tags[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200.')
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), 2, 'Expected 1 result')

    def test_comment_returns_405_on_get_put_patch_delete_and_head(self):
        """
        Test posts/ID/comments endpoint with different methods.
        """
        reset_db()
        p = create_post()
        client = APIClient()
        url = '/api/posts/%s/comments' % p.id
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, 'Expected HTTP 405 on GET.')
        response = client.put(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, 'Expected HTTP 405 on PUT.')
        response = client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, 'Expected HTTP 405 on PATCH.')
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, 'Expected HTTP 405 on DELETE.')
        response = client.head(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, 'Expected HTTP 405 on DELETE.')

    def test_comment_returns_404_on_invalid_post_id(self):
        """
        Test posts/ID/comments endpoint with an invalid post ID.
        """
        reset_db()
        c = APIClient()
        data = {
            "author": {"name": "Test", "email": "t@test.com"},
            "text": "Test"
        }
        response = c.post('/api/posts/1/comments', json.dumps(data), format='json')
        print response.data
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_adds_a_comment_to_post(self):
        """
        Test posts/ID/comments endpoint with an empty database.
        """
        reset_db()
        c = APIClient()
        p = create_post()
        data = {
            "author": {"name": "Test", "email": "t@test.com"},
            "text": "Test"
        }
        response = c.post('/api/posts/%s/comments' % p.id, json.dumps(data), format='json')
        print response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Expected HTTP 201.')


