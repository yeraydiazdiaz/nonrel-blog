"""

    Serializers for RESTful API on the Blog app.

"""

from django.conf import settings
from django.core.paginator import Paginator
from rest_framework import serializers
from rest_framework.pagination import PaginationSerializer
from blog.models import *


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    created_on_readable = serializers.Field(source='created_on_readable')

    class Meta:
        model = Post


class PostPaginationSerializer(PaginationSerializer):

    class Meta:
        object_serializer_class = PostSerializer