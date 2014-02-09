"""

    URLs for blog app

"""

import os
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls import *
from rest_framework.urlpatterns import format_suffix_patterns
import api_views

api_urlpatterns = patterns('blog.api_views',
    url(r'^$', 'api_root'),
    url(r'^posts$', api_views.PostGenericList.as_view(), name='post-list'),
    url(r'^posts/(?P<pk>[0-9]+)$', api_views.PostGenericDetail.as_view(), name='post-detail'),
    url(r'^posts/(?P<pk>[0-9]+)/comments$', api_views.CommentsGenericDetail.as_view(), name='comments'),
    url(r'^posts/tag/(?P<tag>.+)$', api_views.TagGenericList.as_view(), name='tag'),
    url(r'^posts/search/(?P<search_terms>.+)$', api_views.SearchGenericList.as_view(), name='search'),
    url(r'^posts/user/(?P<username>.+)$', api_views.UserGenericList.as_view(), name='user'),
)

api_urlpatterns = format_suffix_patterns(api_urlpatterns)

urlpatterns = patterns(r'blog.views',
    (r'^$', 'home_view'),
    (r'^post/comment/(?P<post_id>.+)/(?P<permalink>.+)$', 'post_view'),
    (r'^post/(?P<post_id>.+)/(?P<permalink>.+)$', 'post_view'),
    (r'^post/(?P<permalink>.+)$', 'post_view'),
    (r'^tag/(?P<tag_name>.+)$', 'tag_view'),
    (r'^login$', 'login_view'),
    (r'^logout$', 'logout_view'),
    (r'^register$', 'register_view'),
    (r'^create_post$', 'create_post_view' ),
    (r'^delete_post/(?P<post_id>.+)$', 'delete_post_view' ),
    (r'^edit_post/(?P<post_id>.+)$', 'edit_post_view' ),
    (r'^search/$', 'search_view' ),
    (r'^load_posts/$', 'load_posts_view' ),
    (r'^api/', include(api_urlpatterns))
)
