"""

    Views module for blog app.

"""

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib.auth.decorators import login_required
from blog.models import Post
from blog.forms import *

def home_view(request):
    """Home view, retrieves the first few posts from the database.

    """
    MAX_HOME_POSTS = 30
    posts = Post.objects.all()[:MAX_HOME_POSTS]
    return render(request, 'home.html', { 'posts': posts })

def post_view(request, post_id, permalink):
    """Post view, attempts to retrieve the post with the id, raising a 404 if not found.
    Also handles the creation of comments.

    """
    try:
        post = Post.objects.get( id=post_id )
    except ObjectDoesNotExist:
        raise Http404
    else:
        if request.method == 'POST': 
            forms = [ AuthorForm(request.POST, error_class=BlogErrorList), 
                     CommentForm(request.POST, error_class=BlogErrorList) ]
            if forms[0].is_valid() and forms[1].is_valid(): 
                post = save_comment( post, *forms )
        else:
            forms = add_css_classes( AuthorForm(), CommentForm() )
        return render(request, 'post.html', { 'post': post, 'forms': forms  })


def tag_view( request, tag_name ):
    """Tag view, shows all posts that include the passed tag.
    
    """
    posts = Post.objects.filter( tags__in= [ tag_name ]  )
    return render(request, 'tag.html', { 'tag': tag_name, 'posts': posts })

def login_view( request ):
    """Login view, handles the creation of the form and authentication of users when the form is submitted.
    
    """
    from django.contrib.auth.forms import AuthenticationForm
    from django.contrib.auth import authenticate, login
    if request.method == 'POST':
        username = request.POST.get( 'username', None )
        password = request.POST.get( 'password', None )
        if username and password:
            user = authenticate( username=username, password=password )
            if user:
                login(request, user)
                return HttpResponseRedirect( request.POST.get( 'next', '/' ) )
        
        form = AuthenticationForm(request.POST, error_class=BlogErrorList)
        return render(request, 'login.html', { 'form': add_css_classes( form ), 'login_failed': True  })
    else:
        form = AuthenticationForm()
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
        form = auth.forms.UserCreationForm( request.POST )
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
            form = auth.forms.UserCreationForm(request.POST, error_class=BlogErrorList)
            return render(request, 'register.html', { 'form': add_css_classes( form ), 'registration_failed': True  })
    else:
        form = auth.forms.UserCreationForm()
        return render(request, 'register.html', { 'form': add_css_classes( form ) })

@login_required
def create_post_view( request ):
    """Create post view

    """
    if request.method == 'POST': 
        form = PostForm(request.POST, error_class=BlogErrorList)
        if form.is_valid(): 
            p = Post.objects.create( title=request.POST['title'],
                                     text=request.POST['text'],
                                     tags=request.POST['tags'].split(),
                                     user_id=request.user.id )
            p.create_permalink_from_title()
            p.save()
            return HttpResponseRedirect('/post/%s/%s' % ( p.id, p.permalink ) )
        
        return render( request, 'create_post.html', { 'form': form } )
    else:
        return render( request, 'create_post.html', { 'form': add_css_classes( PostForm() ) } )

@login_required
def edit_post_view( request, post_id ):
    """Edit post view

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
                p.create_permalink_from_title()
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
    try:
        p = Post.objects.get( id=post_id )
        if request.user.id == p.user_id:
            p.delete()
            return render( request, 'delete_post.html', { 'result' : 'Post deleted correctly.'} )
        else:
            return render( request, 'delete_post.html', { 'error': True, 'result' : 'You are not authorized to delete this post.'} )
    except ObjectDoesNotExist:
        return render( request, 'delete_post.html', { 'error': True, 'result' : 'Post does not exists.'} )
        

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
            
    return forms

def save_comment( post, author_form, comment_form ):
    """Comment form is valid, update the post with the new comment.
    
    """
    a = Author.objects.create( name=author_form.cleaned_data['name'], email=author_form.cleaned_data['email'] )
    c = Comment.objects.create( author=a, text=comment_form.cleaned_data['text'] )
    post.comments.append( c )
    post.save()
    return post