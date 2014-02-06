"""

    Module to host auxiliar functions used across the Blog app tests.

"""

from random import randrange
from itertools import combinations
from django.core import management
from blog.models import *
from django.test.client import Client

# Sample text
lipsum = [
          'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent pharetra erat ut lectus fringilla, nec facilisis urna euismod. Duis eros eros, facilisis ac quam et, vestibulum ultrices dui. Etiam non aliquam orci, at ornare mauris. Praesent porttitor vulputate sapien, a ullamcorper enim eleifend placerat. Morbi dignissim nulla at cursus vulputate. Phasellus magna orci, dignissim pulvinar condimentum aliquam, dignissim eu odio. Nam eu tellus in tortor ornare malesuada eu et nulla. Curabitur ornare rhoncus condimentum. Donec aliquam erat vel justo faucibus eleifend.',
          'Aenean eu commodo nulla. Curabitur eget nibh sem. Curabitur tellus odio, mollis ac aliquet vitae, feugiat eget massa. Fusce at luctus tortor, eget mattis leo. Etiam a ullamcorper lectus, a gravida enim. Curabitur mollis euismod erat et auctor. Nunc libero magna, tempor ut sollicitudin sed, placerat eget sapien. Nunc gravida eget nulla eu ornare. Fusce laoreet, nulla non mattis ornare, felis velit tincidunt felis, et rutrum nunc dolor eu mi. Proin et lacus in justo cursus sollicitudin.',
          'Maecenas varius aliquam libero. Praesent vehicula et nibh euismod cursus. Praesent tristique adipiscing ante, in porttitor ligula consectetur at. Nam porta leo at semper malesuada. Vivamus a aliquam turpis. Vestibulum semper ligula nibh, nec volutpat elit adipiscing a. Praesent non sem ut sapien pharetra eleifend. Phasellus bibendum, dui ut lacinia adipiscing, dui nulla vulputate purus, tempus elementum lacus lectus a enim. Fusce consectetur dapibus nisi. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Donec quis erat at diam bibendum porta. Sed quam quam, fermentum vel commodo eget, ullamcorper nec elit. Sed laoreet ac ante eget pretium. Nullam commodo et urna vel sollicitudin. Quisque vel tempor neque.',
          'Phasellus ut semper purus. Nulla sodales nisi vitae neque lobortis, mattis dictum tortor rhoncus. Vestibulum consequat turpis et tellus mollis, nec dignissim diam elementum. Sed sit amet rutrum urna. Maecenas nec interdum nisi, ac pellentesque nibh. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Duis ac mauris suscipit, consequat purus quis, interdum tortor. Proin viverra convallis lorem, ut laoreet risus ullamcorper lobortis. Suspendisse vel tellus eget nisl elementum mollis ut non tortor. Integer ac congue tortor. Nullam a posuere nunc. Morbi auctor urna sed mollis feugiat. Sed egestas neque non justo cursus, eu ullamcorper neque commodo. Quisque accumsan ipsum in diam tempus suscipit. Praesent fringilla arcu eget tincidunt ullamcorper. Vestibulum elementum a urna ac iaculis.',
          'Donec ut commodo ligula. Integer sit amet tempus diam. Sed tellus libero, egestas at molestie non, gravida non ante. Vestibulum quis nulla nec diam mattis sodales vitae a purus. Aliquam sed enim leo. In gravida purus vel erat elementum, nec faucibus quam vehicula. Ut cursus tellus at sollicitudin mattis. Ut cursus tincidunt tincidunt. Nullam a sapien eget nulla luctus tincidunt. Nunc pretium, nisl eget bibendum eleifend, lacus enim faucibus lacus, egestas semper nisl lectus nec eros. Vivamus adipiscing venenatis dui, ut consequat nibh venenatis et. Quisque eu erat rutrum, sodales nisl nec, dignissim sapien. In ut magna accumsan, pellentesque eros quis, sodales arcu. Sed massa sem, hendrerit non enim et, lobortis venenatis ante. Sed ante nunc, placerat eget metus egestas, feugiat ornare quam. ',
          ]
# Authors list
authors = [ 
           { 'name': 'John', 'email': 'john@example.org' },
           { 'name': 'Paul', 'email': 'paul@example.org' },
           { 'name': 'George', 'email': 'george@example.org' },
           { 'name': 'Ringo', 'email': 'ringo@example.org' }
        ]
# Tags list
tags = [ 'Abbey', 'Yellow', 'Revolver', 'Help' ]

def create_post( title=None, user=None, tags=None):
    """Auxiliar function to create a post.
    Args:
        title: Optional string to be used as title for the post.
    Returns:
        A Post instance with the title or 'Test Post' as title and some sample text.
    """
    if not title:
        title='Test post'

    if not tags:
        tags = get_random_tags()
    p = Post.objects.create( title=title,
                                text=lipsum[ randrange( len(lipsum) ) ],
                                tags=tags
                            )
    if user:
        p.user_id = user.id
    p.create_permalink_from_title()
    p.save()
    return p

def create_comment():
    """Auxiliar function to create a comment using a random selection in the authors list.
    Returns:
        A Comment instance with a random name an email from the authors list and some sample text.
    """
    a = authors[ randrange( len(authors) ) ]
    return Comment( author=Author( name=a['name'], email=a['email'] ), text=lipsum[ randrange( len(lipsum) ) ][:100] )

def create_post_with_comments(title=None, max_comments=5):
    """Auxiliar function to create a post with some comments.
    Args:
        title: Optional string to be used as title.
        max_comments: Optional int to define a maximum number of comments.
    Returns:
        A Post instance with the title or 'Test Post' as title with some sample text and a list of comments.
    """
    p = create_post(title)
    num_comments = randrange( 2, max_comments )
    p.comments = [] 
    for c in xrange(num_comments):
        p.comments.append( create_comment() )
    p.save()
    return p

def reset_db():
    """Auxiliar function to reset the database with default values.
    """
    management.call_command('flush', verbosity=0, interactive=False)
    
def get_random_tags():
    """Get a random list of tags from the tags list.
    """
    size = randrange( len( tags ) )
    random_tags = []
    for i in xrange(size):
        random_tags.append( tags[ randrange( len(tags)) ] )
    return random_tags

def create_user():
    """Creates a user for login tests.
    
    """
    from django.contrib.auth.models import User
    u = User.objects.create_user('John', 'johndoe@example.org', 'foobar')
    u.save()
    return u

def create_and_login_user():
    """Creates a user for login tests.
    
    """
    from django.contrib.auth.models import User
    u = User.objects.create_user('John', 'johndoe@example.org', 'foobar')
    u.save()
    c = Client()
    response = c.post('/login', { 'username': 'John', 'password':'foobar' })
    return response, c, u