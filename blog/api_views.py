"""

    View classes for the RESTful API.

"""

from rest_framework import permissions
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from serializers import *


class PostGenericList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_on')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    paginate_by = settings.REST_FRAMEWORK.get('POST_PAGINATE_BY', 0)


class PostGenericDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


# ENTRY POINT TO API

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'posts': reverse('posts-list', request=request, format=format),
    })