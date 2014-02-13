"""

    View classes for the RESTful API.

"""

from django.conf import settings
from rest_framework import permissions
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_204_NO_CONTENT

from serializers import *


class PostGenericList(generics.ListCreateAPIView):
    """
    API view for lists of Posts, responds to /api/posts.
    By default we sort by inverse creation date and we paginate.
    """
    queryset = Post.objects.all().order_by('-updated_on')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    paginate_by = settings.REST_FRAMEWORK.get('POST_PAGINATE_BY', 0)

    def pre_save(self, obj):
        obj.user_id = self.request.user.id
        obj.save()

    def post_save(self, obj, created=False):
        if created:
            from blog.api_signals import api_create_signal
            api_create_signal.send(sender=None, post_id=obj.id, post_title=obj.title)


class PostGenericDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for detail on Posts, responds to /api/posts/ID.
    Restricted access on update and delete.
    """
    queryset = Post.objects.all().order_by('-updated_on')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def pre_save(self, obj):
        obj.updated_on = timezone.now()

    def post_save(self, obj, created=False):
        from blog.api_signals import api_update_signal
        api_update_signal.send(sender=None, post_id=obj.id, post_title=obj.title)

    def post_delete(self, obj):
        from blog.api_signals import api_delete_signal
        api_delete_signal.send(sender=None, post_id=obj.id, post_title=obj.title)


class TagGenericList(generics.ListAPIView):
    """
    API view for lists of Posts tagged with a particular string, responds to /api/posts/tag/TAG.
    By default we sort by inverse creation date and we paginate.
    """
    lookup_url_kwarg = 'tag'
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    paginate_by = settings.REST_FRAMEWORK.get('POST_PAGINATE_BY', 0)

    def get_queryset(self):
        tag = self.kwargs.get(self.lookup_url_kwarg)
        return Post.objects.filter(tags__in=[tag]).order_by('-updated_on')


class UserGenericList(generics.ListAPIView):
    """
    API view for lists of Posts created by a certain User matching 'username', responds to /api/posts/user/USERNAME.
    By default we sort by inverse creation date and we paginate.
    """
    lookup_url_kwarg = 'username'
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    paginate_by = settings.REST_FRAMEWORK.get('POST_PAGINATE_BY', 0)

    def get_queryset(self):
        from django.contrib.auth.models import User
        username = self.kwargs.get(self.lookup_url_kwarg)
        try:
            u = User.objects.get(username=username)
            return Post.objects.filter(user_id=u.id).order_by('-updated_on')
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return []


class SearchGenericList(generics.ListAPIView):
    """
    API view for search results of Posts, responds to /api/posts/search/TERMS.
    By default we sort by inverse creation date and we paginate.
    """
    lookup_url_kwarg = 'search_terms'
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    paginate_by = settings.REST_FRAMEWORK.get('POST_PAGINATE_BY', 0)

    def get_queryset(self):
        from search.core import search
        search_terms = self.kwargs.get(self.lookup_url_kwarg)
        # force the evaluation of the search RelationIndexQuery result as the pagination doesn't seem to like it
        return [q for q in search(Post, search_terms).order_by('-updated_on')]


class CommentsGenericDetail(generics.CreateAPIView):
    """
    API view for creating comments on a post, responds to /api/posts/ID/comments.
    Restricted access on update and delete.
    """
    serializer_class = CommentSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Post.objects.get(pk=self.kwargs.get(self.lookup_field))

    def pre_save(self, obj):
        try:
            post = Post.objects.get(pk=self.kwargs.get(self.lookup_field))
            if post.comments is None:
                post.comments = [obj]
            else:
                post.comments.append(obj)
            post.save()
            from blog.api_signals import api_comment_signal
            api_comment_signal.send(sender=None, post_id=post.id, post_title=post.title)
        except Post.DoesNotExist:
            from django.http import Http404
            raise Http404


class SiteActivityGenericList(generics.ListAPIView):
    """
    API view for SiteActivities, responds to /api/siteactivities.
    By default we sort by inverse creation date and we paginate.
    """
    lookup_url_kwarg = 'timestamp'
    serializer_class = SiteActivitySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        timestamp = self.kwargs.get(self.lookup_url_kwarg)
        if timestamp:
            import datetime
            dt = datetime.datetime.fromtimestamp(int(timestamp))
            return SiteActivity.objects.filter(created_on__gt=dt).order_by('-created_on')
        else:
            return SiteActivity.objects.all().order_by('-created_on')


@api_view(('GET',))
def all_tags(request, format=None):
    """
    All-tags endpoint, returns a list of the unique tags in the posts.
    """
    if Post.objects.count():
        return Response(list(set([t for p in Post.objects.all() for t in p.tags])))
    else:
        return Response('', status=HTTP_204_NO_CONTENT)

@api_view(('GET',))
def api_root(request, format=None):
    """
    Entry point to API for use on the browsable API REST Framework feature.
    """
    return Response({
        'post': reverse('post-list', request=request, format=format),
        'site-activities': reverse('site-activities', request=request, format=format),
        'all-tags': reverse('all-tags', request=request, format=format),
    })