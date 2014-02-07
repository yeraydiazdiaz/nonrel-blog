"""

    Serializers for RESTful API on the Blog app.

"""

from rest_framework import serializers
from rest_framework.pagination import PaginationSerializer
from blog.models import *


class AuthorSerializer(serializers.ModelSerializer):
    """
    Base ModelSerializer for Author model
    """
    class Meta:
        model = Author


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model using a single nested relationship with Author.
    """
    author = AuthorSerializer()
    created_on_readable = serializers.Field(source='created_on_readable')

    class Meta:
        model = Comment
        fields = ('author', 'text', 'created_on_readable')


class PostSerializer(serializers.ModelSerializer):
    """
    Post serializer, adds nested comments and readable date from Datetime object from model declaration.
    """
    comments = CommentSerializer(many=True, required=False)
    permalink = serializers.CharField(required=False)
    tags = serializers.CharField(required=False)
    created_on_readable = serializers.Field(source='created_on_readable')

    def validate_tags(self, attrs, source):
        attrs[source] = attrs[source].split()
        return attrs

    class Meta:
        model = Post
        fields = ('id', 'title', 'permalink', 'user_id', 'text', 'tags', 'comments', 'created_on_readable')


class PostPaginationSerializer(PaginationSerializer):
    """
    Paginated serializer for Post, the pagination parameter is defined in the settings as it's used by the vanilla
    Django system.
    """

    class Meta:
        object_serializer_class = PostSerializer