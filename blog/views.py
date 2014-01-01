"""

    Views module for blog app.

"""

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from blog.models import Post
from blog.forms import *

INITIAL_POSTS = 2

def home_view(request):
    """Home view, retrieves the first few posts from the database.

    """
    posts = Post.objects.all().order_by('-created_on')[:INITIAL_POSTS]
    total_posts = Post.objects.all().count()
    return render(request, 'home.html', { 'posts': posts, 'total_posts': total_posts })

def post_view(request, post_id=None, permalink=None):
    """Post view, attempts to retrieve the post with the id, raising a 404 if not found. Also handles the creation of comments.
    Args:
        post_id: Primary key of the post to be shown.
        permalink: String containing the permalink for the post, if captured.
    """
    try:
        if post_id:
            post = Post.objects.get( id=post_id )
        elif permalink:
            post = Post.objects.get( permalink=permalink )
        else:
            raise Http404
    except ObjectDoesNotExist:
        raise Http404
    else:
        if request.method == 'POST': 
            forms = [ AuthorForm(request.POST, error_class=BlogErrorList), 
                     CommentForm(request.POST, error_class=BlogErrorList) ]
            forms = add_css_classes( *forms )
            if forms[0].is_valid() and forms[1].is_valid(): 
                post = save_comment( post, *forms )
        else:
            forms = add_css_classes( AuthorForm(error_class=BlogErrorList), CommentForm(error_class=BlogErrorList) )
        return render(request, 'post.html', { 'post': post, 'forms': forms  })


def tag_view( request, tag_name ):
    """Tag view, shows all posts that include the passed tag.
    Args:
        tag_name: String containing a possible tag.
    
    """
    total_posts = Post.objects.filter( tags__in= [ tag_name ]  ).count()
    posts = Post.objects.filter( tags__in= [ tag_name ]  )[:INITIAL_POSTS]
    return render(request, 'tag.html', { 'terms': tag_name, 'posts': posts, 'total_posts': total_posts })

def login_view( request ):
    """Login view, handles the creation of the form and authentication of users when the form is submitted.
    
    """
    import django.contrib.auth as auth
    if request.method == 'POST':
        form = auth.forms.AuthenticationForm(data=request.POST, error_class=BlogErrorList)
        if form.is_valid():
            username = request.POST.get( 'username', None )
            password = request.POST.get( 'password', None )
            user = auth.authenticate( username=username, password=password )
            if user:
                auth.login(request, user)
                return HttpResponseRedirect( request.POST.get( 'next', '/' ) )

        return render(request, 'login.html', { 'form': add_css_classes( form ), 'login_failed': True  })
    else:
        form = auth.forms.AuthenticationForm(error_class=BlogErrorList)
        next = request.GET.get('next', None)
        if next:
            import django.forms as forms 
            form.fields['next'] = forms.CharField( widget=forms.HiddenInput( attrs={ 'value': next }) )
            
    return render(request, 'login.html', { 'form': add_css_classes( form ) })

def logout_view( request ):
    """Logout view.
    
    """
    from django.contrib.auth import logout
    logout( request )
    return HttpResponseRedirect( '/' )

def register_view( request ):
    """Register view, handles password matching errors and creation of new users.
    
    """
    import django.contrib.auth as auth
    if request.method == 'POST':
        form = auth.forms.UserCreationForm( request.POST, error_class=BlogErrorList )
        if form.is_valid():
            username = request.POST.get( 'username', None )
            password1 = request.POST.get( 'password1', None )
            password2 = request.POST.get( 'password2', None )
            if username and password1 and password2 and password1 == password2:
                auth.models.User.objects.create_user( username=username, password=password1 )
                user = auth.authenticate( username=username, password=password1 )
                if user is not None:
                    auth.login(request, user)
                    return HttpResponseRedirect( request.REQUEST.get( 'next', '/' ) )
        else:
            return render(request, 'register.html', { 'form': add_css_classes( form )  })
    else:
        form = auth.forms.UserCreationForm( error_class=BlogErrorList )
        return render(request, 'register.html', { 'form': add_css_classes( form ) })

@login_required
def create_post_view( request ):
    """Create post view, handles the form and validation of submitted data. 

    """
    if request.method == 'POST': 
        form = PostForm(request.POST, error_class=BlogErrorList)
        if form.is_valid(): 
            p = Post.objects.create( title=request.POST['title'],
                                     text=request.POST['text'],
                                     tags=request.POST['tags'].split(),
                                     user_id=request.user.id )
            p.save()
            return HttpResponseRedirect('/post/%s/%s' % ( p.id, p.permalink ) )
        
        return render( request, 'create_post.html', { 'form': form } )
    else:
        return render( request, 'create_post.html', { 'form': add_css_classes( PostForm(error_class=BlogErrorList) ) } )

@login_required
def edit_post_view( request, post_id ):
    """Edit post view, handles submission of forms and renders a result message if the post does not exist.
    Args:
        post_id: Primary key of the post to be edited.
    """
    try:
        p = Post.objects.get( id=post_id )
        if request.method == 'POST': 
            form = PostForm(request.POST, error_class=BlogErrorList)
            if form.is_valid(): 
                p.title=request.POST['title']
                p.text=request.POST['text']
                p.tags=request.POST.get('tags', '').split()
                p.user_id=request.user.id
                p.save()
                return HttpResponseRedirect('/post/%s/%s' % ( p.id, p.permalink ) )
        else:
            form = PostForm( initial= {
                                'title': p.title,
                                'text': p.text,
                                'tags': ' '.join(p.tags)
                            } )

        return render( request, 'edit_post.html', { 'form': add_css_classes( form ) } )

    except ObjectDoesNotExist:
        return render( request, 'edit_post.html', { 'error': True, 'result' : 'Post does not exist.'} )
        

@login_required
def delete_post_view( request, post_id ):
    """Delete post view, handles deletion of posts displaying a confirmation or error message.
    Args:
        post_id: Primary key of the post to be deleted.
    """
    try:
        p = Post.objects.get( id=post_id )
        if request.user.id == p.user_id:
            p.delete()
            return render( request, 'delete_post.html', { 'result' : 'Post deleted correctly.'} )
        else:
            return render( request, 'delete_post.html', { 'error': True, 'result' : 'You are not authorized to delete this post.'} )
    except ObjectDoesNotExist:
        return render( request, 'delete_post.html', { 'error': True, 'result' : 'Post does not exists.'} )


def search_view( request ):
    """Search view, handles searching on posts based on arbitrary strings. See search_indexes for details.

    """
    from search.core import search
    search_terms = request.GET.get('q', None)
    if search_terms:
        total_posts = search( Post, search_terms ).order_by('-created_on').count()
        sliced_posts = search( Post, search_terms ).order_by('-created_on')[:INITIAL_POSTS]
    else:
        total_posts = 0
        sliced_posts = None
    return render( request, 'search.html', { 'posts': sliced_posts, 'total_posts': total_posts, 'terms': search_terms } )

def load_posts_view( request ):
    """Load posts view, handles asynchronous queries to retrieve more posts.

    """
    import json
    if request.method == 'GET':
        results, start = get_more_posts( request.GET )
        json_result = json.dumps( { 'posts': results,
                                   'start': start 
                                } )
        return HttpResponse(json_result, mimetype='application/json')    
    else:
        return HttpResponse('', mimetype='application/json')

### Auxiliar functions 

def add_css_classes( *forms ):
    """Adds custom classes to all widgets in the form. Used to style the forms using bootstrap classes.
    
    """
    for form in forms:
        try:
            for field in form.fields:
                form.fields[field].widget.attrs.update( { 'class': 'form-control input-sm' } )
        except AttributeError:
            form.field.widget.attrs.update( { 'class': 'form-control input-sm' } )

        if len(forms) == 1:
            return form     # return the single form rather that a 1-sized tuple
    
    return forms

def save_comment( post, author_form, comment_form ):
    """Comment form is valid, update the post with the new comment.
    
    """
    a = Author.objects.create( name=author_form.cleaned_data['name'], email=author_form.cleaned_data['email'] )
    c = Comment.objects.create( author=a, text=comment_form.cleaned_data['text'] )
    post.comments.append( c )
    post.save()
    return post

def get_more_posts( GET ):
    """Function to retrieve additional posts.
    """
    from django.template import Template, Context, loader
    page = GET.get('page', None)
    start = int( GET.get('start', 0) )
    total = int( GET.get('total', 0) )
    if start and total and page and start < total:
        end = start+INITIAL_POSTS if start+INITIAL_POSTS < total else total
        if page == 'home':
            posts = Post.objects.all().order_by('-created_on')[start:end]
        elif page == 'search':
            from search.core import search
            search_terms = GET['terms']
            raw_posts = search( Post, search_terms ).order_by('-created_on')
            posts = [ raw_posts[p] for p in range(start,end) ] # slicing a search result seems to give empty lists?
        elif page == 'tag':
            tag_name = GET['terms']
            posts = Post.objects.filter( tags__in= [ tag_name ]  )[start:end]
        else:
            return None
    
        t = loader.get_template('post_list.html')
        if len(posts) == 0:
            return '', 0
        else:
            d = { 'posts': posts }
            
        return t.render( Context( d ) ), start+INITIAL_POSTS
    else:
        return '', 0