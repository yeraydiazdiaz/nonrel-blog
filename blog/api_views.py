"""

    View classes for the RESTful API.

"""

from django.conf import settings
from rest_framework import permissions
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from serializers import *


class PostGenericList(generics.ListCreateAPIView):
    """
    API view for lists of Posts, responds to /api/posts.
    By default we sort by inverse creation date and we paginate.
    """
    queryset = Post.objects.all().order_by('-created_on')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    paginate_by = settings.REST_FRAMEWORK.get('POST_PAGINATE_BY', 0)

    def pre_save(self, obj):
        obj.user_id = self.request.user.id
        obj.save()


class PostGenericDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for detail on Posts, responds to /api/posts/ID.
    Restricted access on update and delete.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


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
        return Post.objects.filter(tags__in=[tag])


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
            elif post.comments == []:
                post.comments.append(obj)
            post.save()
        except Post.DoesNotExist:
            from django.http import Http404
            raise Http404


@api_view(('GET',))
def api_root(request, format=None):
    """
    Entry point to API
    """
    return Response({
        'post': reverse('post-list', request=request, format=format),
    })