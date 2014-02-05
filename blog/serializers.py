"""

    Serializers for RESTful API on the Blog app.

"""

from rest_framework import serializers
from rest_framework.pagination import PaginationSerializer
from blog.models import *


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    class Meta:
        model = Post


class PostPaginationSerializer(PaginationSerializer):
    class Meta:
        object_serializer_class = PostSerializer