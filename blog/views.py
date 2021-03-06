"""

    Views module for blog app.

"""

from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from blog.forms import *

INITIAL_POSTS = settings.REST_FRAMEWORK.get('POST_PAGINATE_BY', 0)
MESSAGE_TAGS = {messages.ERROR: 'danger'}


def home_view(request):
    """
    Home view, retrieves the first few posts from the database.
    """
    import serializers
    from rest_framework.renderers import JSONRenderer
    posts = Post.objects.all().order_by('-sticky', '-updated_on')
    total_posts = posts.count()
    paginator = Paginator(posts, INITIAL_POSTS)
    paged_posts = paginator.page(1)
    serializer = serializers.PostPaginationSerializer(
        paged_posts, context={'request': request})
    paginated_models_json = JSONRenderer().render(serializer.data['results'])
    return render(request, 'home.html', {'posts': paged_posts,
                                         'total_posts': total_posts,
                                         'models_json': paginated_models_json,
                                         'next': serializer.data['next'],
                                         })


def post_view(request, post_id=None, permalink=None):
    """
    Post view, attempts to retrieve the post with the id,
    raising a 404 if not found.
    Also handles the creation of comments.
    Args:
        post_id: Primary key of the post to be shown.
        permalink: String containing the permalink for the post, if captured.
    """
    try:
        if post_id:
            post = Post.objects.get(id=post_id)
        elif permalink:
            post = Post.objects.get(permalink=permalink)
        else:
            raise Http404
    except Post.DoesNotExist:
        raise Http404
    else:
        if request.method == 'POST':
            forms = [AuthorForm(request.POST, error_class=BlogErrorList),
                     CommentForm(request.POST, error_class=BlogErrorList)]
            forms = add_css_classes(*forms)
            if forms[0].is_valid() and forms[1].is_valid():
                messages.success(request, 'Comment created successfully.')
                post = save_comment(post, *forms)
        else:
            forms = add_css_classes(
                AuthorForm(error_class=BlogErrorList), CommentForm(error_class=BlogErrorList))
        return render(request, 'post.html', {'post': post, 'forms': forms})


def tag_view(request, tag_name):
    """
    Tag view, shows all posts that include the passed tag.
    Args:
        tag_name: String containing a possible tag.
    """
    total_posts = Post.objects.filter(tags__in=[tag_name]).count()
    posts = Post.objects.filter(tags__in=[tag_name])[:INITIAL_POSTS]
    return render(request, 'tag.html', {'terms': tag_name,
                                        'posts': posts,
                                        'total_posts': total_posts})


def login_view(request):
    """
    Login view, handles the creation of the form and
    authentication of users when the form is submitted.
    """
    import django.contrib.auth as auth
    if request.method == 'POST':
        form = auth.forms.AuthenticationForm(
            data=request.POST, error_class=BlogErrorList)
        if form.is_valid():
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(request.POST.get('next', '/'))
            else:
                data = request.POST
                login_form = auth.forms.AuthenticationForm(
                    data, error_class=BlogErrorList)
                return render(request, 'login.html', {'form': add_css_classes(login_form), 'login_failed': True})
        else:
            return render(request, 'login.html', {'form': add_css_classes(form), 'login_failed': True})
    else:
        form = auth.forms.AuthenticationForm(error_class=BlogErrorList)
        next = request.GET.get('next', None)
        if next:
            import django.forms as forms
            form.fields['next'] = forms.CharField(
                widget=forms.HiddenInput(attrs={'value': next}))

    return render(request, 'login.html', {'form': add_css_classes(form)})


def logout_view(request):
    """
    Logout view.
    """
    from django.contrib.auth import logout
    logout(request)
    return HttpResponseRedirect('/')


def register_view(request):
    """
    Register view, handles password matching errors and creation of new users.
    """
    import django.contrib.auth as auth
    if request.method == 'POST':
        form = auth.forms.UserCreationForm(
            request.POST, error_class=BlogErrorList)
        if form.is_valid():
            username = request.POST.get('username', None)
            password1 = request.POST.get('password1', None)
            user = auth.models.User.objects.create_user(
                username=username, password=password1)
            # pass the id of the created user to ensure strong consistency by
            # fetching through ID rather than a normal username query
            user = auth.authenticate(
                username=username, password=password1, id=user.id)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(request.REQUEST.get('next', '/'))
            else:
                login_form = auth.forms.AuthenticationForm(
                    data={'username': username,
                          'password': password1},
                    error_class=BlogErrorList)
                return render(request, 'login.html', {'form': add_css_classes(login_form)})
        else:
            return render(request, 'register.html', {'form': add_css_classes(form)})
    else:
        form = auth.forms.UserCreationForm(error_class=BlogErrorList)
        return render(request, 'register.html', {'form': add_css_classes(form)})


@login_required
def create_post_view(request):
    """
    Create post view, handles the form and validation of submitted data.
    """
    if request.method == 'POST':
        form = PostForm(request.POST, error_class=BlogErrorList)
        if form.is_valid():
            p = Post.objects.create(title=request.POST['title'],
                                    text=request.POST['text'],
                                    tags=request.POST['tags'].split(),
                                    user_id=request.user.id)
            p.save()
            messages.success(request, 'Post created successfully.')
            return HttpResponseRedirect('/post/%s/%s' % (p.id, p.permalink))

        return render(request, 'create_post.html', {'form': add_css_classes(form)})
    else:
        return render(request, 'create_post.html', {'form': add_css_classes(PostForm(error_class=BlogErrorList))})


@login_required
def edit_post_view(request, post_id):
    """
    Edit post view, handles submission of forms
    and renders a result message if the post does not exist.
    Args:
        post_id: Primary key of the post to be edited.
    """
    p = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, error_class=BlogErrorList)
        if form.is_valid():
            p.title = request.POST['title']
            p.text = request.POST['text']
            p.tags = request.POST.get('tags', '').split()
            p.user_id = request.user.id
            p.save()
            messages.success(request, 'Post updated correctly.')
            return HttpResponseRedirect('/post/%s/%s' % (p.id, p.permalink))
    else:
        form = PostForm(initial={
            'title': p.title,
            'text': p.text,
            'tags': ' '.join(p.tags)
        })
    return render(request, 'edit_post.html', {'form': add_css_classes(form)})


@login_required
def delete_post_view(request, post_id):
    """Delete post view, handles deletion of posts displaying a
    confirmation or error message.
    Args:
        post_id: Primary key of the post to be deleted.
    """
    p = get_object_or_404(Post, pk=post_id)
    if request.user.id == p.user_id:
        p.delete()
        messages.success(request, 'Post deleted correctly.')
        return HttpResponseRedirect('/')
    else:
        return render(request, 'delete_post.html', {'error': True,
                                                    'result': 'You are not authorized to delete this post.'})


def search_view(request):
    """Search view, handles searching on posts based on arbitrary strings.
    See search_indexes for details.

    """
    from search.core import search
    search_terms = request.GET.get('q', None)
    if search_terms:
        total_posts = search(Post, search_terms).order_by(
            '-sticky', '-updated_on').count()
        sliced_posts = search(Post, search_terms).order_by(
            '-sticky', '-updated_on')[:INITIAL_POSTS]
    else:
        total_posts = 0
        sliced_posts = None
    return render(request, 'search.html', {'posts': sliced_posts,
                                           'total_posts': total_posts,
                                           'terms': search_terms})


def load_posts_view(request):
    """Load posts view, handles asynchronous queries to retrieve more posts.

    """
    import json
    if request.method == 'GET':
        results, start = get_more_posts(request.GET)
        json_result = json.dumps({'posts': results,
                                  'start': start
                                  })
        return HttpResponse(json_result, mimetype='application/json')
    else:
        return HttpResponse('', mimetype='application/json')


# Auxiliar functions
def add_css_classes(*forms):
    """
    Adds custom classes to all widgets in the form.
    Used to style the forms using bootstrap classes.
    """
    for form in forms:
        try:
            for field in form.fields:
                form.fields[field].widget.attrs.update(
                    {'class': 'form-control input-sm'})
        except AttributeError:
            form.field.widget.attrs.update(
                {'class': 'form-control input-sm'})

        if len(forms) == 1:
            # return the single form rather that a 1-sized tuple
            return form

    return forms


def save_comment(post, author_form, comment_form):
    """
    Comment form is valid, update the post with the new comment.
    """
    from blog.api_signals import api_comment_signal
    a = Author.objects.create(name=author_form.cleaned_data[
                              'name'], email=author_form.cleaned_data['email'])
    c = Comment.objects.create(
        author=a, text=comment_form.cleaned_data['text'])
    if not post.comments:
        post.comments = [c]
    else:
        post.comments.append(c)
    post.save()
    api_comment_signal.send(
        sender=None, post_id=post.id, post_title=post.title)
    return post


def get_more_posts(GET):
    """
    Function to retrieve additional posts.
    """
    from django.template import Context, loader
    page = GET.get('page', None)
    start = int(GET.get('start', 0))
    total = int(GET.get('total', 0))
    if start and total and page and start < total:
        end = start + INITIAL_POSTS if start + INITIAL_POSTS < total else total
        if page == 'home':
            posts = Post.objects.all().order_by(
                '-sticky', '-updated_on')[start:end]
        elif page == 'search':
            from search.core import search
            search_terms = GET['terms']
            raw_posts = search(Post, search_terms).order_by(
                '-sticky', '-updated_on')
            # slicing a search result seems to give empty lists?
            posts = [raw_posts[p] for p in range(start, end)]
        elif page == 'tag':
            tag_name = GET['terms']
            posts = Post.objects.filter(tags__in=[tag_name])[start:end]
        else:
            return None

        t = loader.get_template('post_list.html')
        if len(posts) == 0:
            return '', 0
        else:
            d = {'posts': posts}

        return t.render(Context(d)), start + INITIAL_POSTS
    else:
        return '', 0
