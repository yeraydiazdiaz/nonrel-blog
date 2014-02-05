"""

    RESTful API specific tests.

"""

import json
from django.test import TestCase
from blog.models import *
from blog.test_aux import *
from rest_framework import status

class BlogAPITests(TestCase):

    def test_post_list_returns_empty_on_empty_db(self):
        """
        Test posts endpoint with an empty database.
        """
        reset_db()
        c = Client()
        response = c.get('/api/posts')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200.')
        self.assertEquals(len(json.loads(response.content)), 0, 'Expected 0 results')

    def test_post_list_returns_one_post(self):
        """
        Test posts endpoint with an empty database.
        """
        reset_db()
        p = create_post()
        c = Client()
        response = c.get('/api/posts')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200.')
        self.assertEquals(len(json.loads(response.content)), 1, 'Expected 1 result')