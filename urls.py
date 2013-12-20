"""

    urls.py for non-rel blog.

"""

import os
from django.conf.urls.defaults import *
from django.contrib import admin
import dbindexer
from django.conf import settings 
from django.conf.urls.static import static

handler500 = 'djangotoolbox.errorviews.server_error'

# django admin
admin.autodiscover()

# search for dbindexes.py in all INSTALLED_APPS and load them
dbindexer.autodiscover()

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ('^$', 'blog.views.home_view'),
    ('^post/comment/(?P<post_id>.+)/(?P<permalink>.+)$', 'blog.views.post_view'),
    ('^post/(?P<post_id>.+)/(?P<permalink>.+)$', 'blog.views.post_view'),
    ('^tag/(?P<tag_name>.+)$', 'blog.views.tag_view'),
    ('^login$', 'blog.views.login_view'),
    ('^logout$', 'blog.views.logout_view'),
    ('^register$', 'blog.views.register_view'),
    ('^create_post$', 'blog.views.create_post_view' ),
    ('^delete_post/(?P<post_id>.+)$', 'blog.views.delete_post_view' ),
    ('^edit_post/(?P<post_id>.+)$', 'blog.views.edit_post_view' ),
) + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]) 

