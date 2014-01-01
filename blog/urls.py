"""

	URLs for blog app

"""

import os
from django.conf.urls.defaults import *
from django.contrib import admin

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
)