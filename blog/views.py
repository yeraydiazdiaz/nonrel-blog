"""

    Views module for blog app.

"""

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from blog.models import Post

def home(request):
    """Home view, retrieves the first few posts from the database.

    """
    MAX_HOME_POSTS = 30
    posts = Post.objects.all()[:MAX_HOME_POSTS]
    return render(request, 'home.html', { 'posts': posts })

def post(request, id, permalink):
    """Post view, attempts to retrieve the post with the id, raising a 404 if not found.

    """
    try:
        post = Post.objects.get( id=id )
        return render(request, 'post.html', { 'post': post })
    except ObjectDoesNotExist:
        raise Http404
