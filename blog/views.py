"""

    Views module for blog app.

"""

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from blog.models import Post
from blog.forms import *

def home(request):
    """Home view, retrieves the first few posts from the database.

    """
    MAX_HOME_POSTS = 30
    posts = Post.objects.all()[:MAX_HOME_POSTS]
    return render(request, 'home.html', { 'posts': posts })

def post(request, id_, permalink):
    """Post view, attempts to retrieve the post with the id, raising a 404 if not found.

    """
    try:
        post = Post.objects.get( id=id_ )
    except ObjectDoesNotExist:
        raise Http404
    else:
        if request.method == 'POST': 
            forms = [ AuthorForm(request.POST), CommentForm(request.POST) ]
            if forms[0].is_valid() and forms[1].is_valid(): 
                post = save_comment( post, *forms )
        else:
            forms = [ AuthorForm(), CommentForm() ]
        return render(request, 'post.html', { 'post': post, 'forms': forms })

def save_comment( post, author_form, comment_form ):
    """Form is valid, update the post with the new comment.
    
    """
    a = Author.objects.create( name=author_form.cleaned_data['name'], email=author_form.cleaned_data['email'] )
    c = Comment.objects.create( author=a, text=comment_form.cleaned_data['text'] )
    post.comments.append( c )
    post.save()
    return post