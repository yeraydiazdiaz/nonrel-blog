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
    (r'^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'', include('blog.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]) 
