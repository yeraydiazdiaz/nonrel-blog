"""

    RESTful API specific tests.

"""

from rest_framework.test import APITestCase
import json, datetime, time
from django.utils import timezone
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
        response = c.post('/api/posts/1/comments', data, format='json')
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
        response = c.post('/api/posts/%s/comments' % p.id, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Expected HTTP 201.')
        p = Post.objects.get()
        self.assertEqual(len(p.comments), 1)

    def test_POST_posts_is_restricted_to_authenticated_users(self):
        """
        Test POST on /api/posts to create new posts is restricted to authenticated users.
        """
        reset_db()
        c = APIClient()
        data = {
            "author": {"name": "Test", "email": "t@test.com"},
            "text": "Test"
        }
        response = c.post('/api/posts', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, 'Expected HTTP 403.')

    def test_POST_posts_creates_post(self):
        """
        Test POST on /api/posts adds a new post correctly.
        """
        reset_db()
        u = create_user()
        c = APIClient()
        c.login(username=u.username, password='foobar')
        data = {
            "title": "Test post title",
            "text": "Test post text",
            "tags": ['tag1', 'tag2']
        }
        response = c.post('/api/posts', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Expected HTTP 201.')
        self.assertEqual(Post.objects.count(), 1, 'Expected one post after creation.')
        p = Post.objects.get()
        self.assertEqual(len(p.tags), 2, 'Expected two tags.')

    def test_DELETE_posts_is_restricted_to_authenticated_users(self):
        """
        Test DELETE on a post is restricted to authenticated users.
        """
        reset_db()
        c = APIClient()
        p = create_post()
        response = c.delete('/api/posts/%s' % p.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, 'Expected HTTP 403.')

    def test_DELETE_posts_deletes_the_post(self):
        """
        Test DELETE on a post is restricted to authenticated users.
        """
        reset_db()
        c = APIClient()
        u = create_user()
        p = create_post(user=u)
        c.login(username=u.username, password='foobar')
        response = c.delete('/api/posts/%s' % p.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'Expected HTTP 204.')
        self.assertEqual(Post.objects.count(), 0, 'Expected no posts.')

    def test_search_endpoint_returns_no_results_on_empty_db(self):
        """
        Test search endpoint on an empty database.
        """
        reset_db()
        c = APIClient()
        response = c.get('/api/posts/search/foobar')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200.')
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), 0, 'Expected no results')

    def test_search_endpoint_returns_one_result_correctly(self):
        """
        Test search endpoint with a single matching post.
        """
        reset_db()
        c = APIClient()
        u = create_user()
        p = create_post(title='foobar', user=u)
        response = c.get('/api/posts/search/foobar')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200.')
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), 1, 'Expected 1 result')

    def test_search_endpoint_returns_no_results_if_no_match(self):
        """
        Test search endpoint with no matching post.
        """
        reset_db()
        c = APIClient()
        u = create_user()
        p = create_post(title='Test title', user=u)
        response = c.get('/api/posts/search/foobar')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200.')
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), 0, 'Expected no results')

    def test_user_endpoint_returns_no_results_on_empty_db(self):
        """
        Test user endpoint with an empty database.
        """
        reset_db()
        c = APIClient()
        u = create_user()
        response = c.get('/api/posts/user/' + u.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200 got %s.' % response.status_code)
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), 0, 'Expected no results')

    def test_user_endpoint_returns_one_result_with_one_post(self):
        """
        Test user endpoint with one matching post.
        """
        reset_db()
        c = APIClient()
        u = create_user()
        p = create_post(user=u)
        response = c.get('/api/posts/user/' + u.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200 got %s.' % response.status_code)
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), 1, 'Expected 1 result')
        self.assertEquals(content['results'][0]['user_id'], u.id,
                          'Expected user ids to match, got %s and expected %s' % (content['results'][0]['user_id'], u.id))

    def test_user_endpoint_returns_no_results_if_user_has_no_posts(self):
        """
        Test user endpoint with one non-matching post.
        """
        reset_db()
        c = APIClient()
        joe = create_user(username='Joe')
        john = create_user()
        create_post(user=john)
        response = c.get('/api/posts/user/' + joe.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200 got %s.' % response.status_code)
        content = json.loads(response.content)
        self.assertEquals(len(content['results']), 0, 'Expected no results')

    def test_user_endpoint_returns_several_matching_results(self):
        """
        Test user endpoint with one matching post.
        """
        reset_db()
        c = APIClient()
        joe = create_user(username='Joe')
        john = create_user()
        for i in xrange(3):
            if i % 2 == 0:
                create_post(user=joe)
            else:
                create_post(user=john)

        expected_results = 2
        response = c.get('/api/posts/user/' + joe.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200 got %s.' % response.status_code)
        content = json.loads(response.content)
        self.assertEquals(content['count'], expected_results, 'Expected 2 result, got %s' % content['count'])
        for i in xrange(expected_results):
            self.assertEquals(content['results'][i]['user_id'], joe.id,
                          'Expected user ids to match, got %s and expected %s' % (content['results'][i]['user_id'], joe.id))

    def test_site_activities_endpoint_returns_no_results_on_empty_db(self):
        """
        Test site activities endpoint with empty db.
        """
        reset_db()
        c = APIClient()
        response = c.get('/api/siteactivities')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200 got %s.' % response.status_code)
        content = json.loads(response.content)
        self.assertEquals(len(content), 0, 'Expected no results')

    def test_site_activities_endpoint_returns_results_on_activities(self):
        """
        Test site activities endpoint with empty db.
        """
        reset_db()
        c = APIClient()
        u = create_user()
        c.login(username=u.username, password='foobar')
        data = {
            "title": "Test post title",
            "text": "Test post text",
            "tags": ['tag1', 'tag2']
        }
        c.post('/api/posts', data, format='json')
        time.sleep(1)
        data['title'] = "Second test post title"
        c.post('/api/posts', data, format='json')
        expected = 2
        request_url = '/api/siteactivities'
        response = c.get(request_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200 got %s.' % response.status_code)
        content = json.loads(response.content)
        self.assertEquals(len(content), expected, 'Expected %s results, got %s' % (expected, len(content)))
        request_url = '/api/siteactivities/%s' % timezone.now().strftime('%s')
        response = c.get(request_url)
        expected = 1
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Expected HTTP 200 got %s.' % response.status_code)
        content = json.loads(response.content)
        self.assertEquals(len(content), expected, 'Expected %s results, got %s' % (expected, len(content)))