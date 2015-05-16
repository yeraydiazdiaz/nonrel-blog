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
    created_on_readable = serializers.Field(source='created_on')

    def transform_created_on_readable(self, obj, value):
        return value.strftime('%A %d %b %Y - %H:%M:%S')

    class Meta:
        model = Comment
        fields = ('author', 'text', 'created_on_readable')


class PostSerializer(serializers.ModelSerializer):
    """
    Post serializer, adds nested comments and readable date from Datetime
    object from model declaration.
    """
    user_id = serializers.Field(source='user_id')
    user_name = serializers.Field(source='user_id')
    permalink = serializers.Field(source='permalink')
    comments = CommentSerializer(many=True, required=False)
    tags = serializers.CharField(source='tags', required=False)
    created_on_readable = serializers.Field(source='created_on')
    updated_on_readable = serializers.Field(source='updated_on')
    timestamp = serializers.Field(source='updated_on')

    def transform_user_name(self, obj, value):
        from django.contrib.auth.models import User
        return User.objects.get(pk=value).username

    def transform_created_on_readable(self, obj, value):
        return value.strftime('%A %d %b %Y - %H:%M:%S')

    def transform_updated_on_readable(self, obj, value):
        return value.strftime('%A %d %b %Y - %H:%M:%S')

    def transform_tags(self, obj, value):
        if type(value) != list:
            return []
        else:
            return value

    def transform_timestamp(self, obj, value):
        import calendar
        return int(calendar.timegm(value.utctimetuple()))

    def validate_tags(self, attrs, source):
        try:
            # safely eval the array of tags into a Python native array.
            import ast
            tags = ast.literal_eval(attrs[source])
            attrs[source] = tags
        except AttributeError:
            attrs[source] = []
        except KeyError:
            attrs['tags'] = []

        return attrs

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'permalink', 'user_name', 'user_id', 'text',
            'tags', 'comments', 'created_on_readable', 'updated_on_readable',
            'timestamp', 'sticky'
        )


class PostPaginationSerializer(PaginationSerializer):
    """
    Paginated serializer for Post, the pagination parameter is defined in the
    settings as it's used by the vanilla Django system.
    """

    class Meta:
        object_serializer_class = PostSerializer


class SiteActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for SiteActivityModel model.
    """
    timestamp = serializers.Field(source='created_on')
    created_on_readable = serializers.Field(source='created_on')

    def transform_created_on_readable(self, obj, value):
        return value.strftime('%A %d %b %Y - %H:%M:%S')

    def transform_timestamp(self, obj, value):
        return value.strftime('%s')

    class Meta:
        model = SiteActivity
