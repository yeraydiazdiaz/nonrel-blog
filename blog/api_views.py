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


class PostGenericDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for detail on Posts, responds to /api/posts/ID.
    Restricted access on update and delete.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


@api_view(('GET',))
def api_root(request, format=None):
    """
    Entry point to API
    """
    return Response({
        'posts': reverse('posts-list', request=request, format=format),
    })