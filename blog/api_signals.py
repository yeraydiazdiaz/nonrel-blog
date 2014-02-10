"""

api_signals.py
Definition of custom signals and receivers to be fired by the API views.
All of them create different types of SiteActivity instances that will later
be read by the SiteActivity view in the UI.

"""

from django.dispatch import receiver
import django.dispatch
from blog.models import SiteActivity

api_comment_signal = django.dispatch.Signal(providing_args=['post_id', 'post_title'])
api_create_signal = django.dispatch.Signal(providing_args=['post_id', 'post_title'])
api_update_signal = django.dispatch.Signal(providing_args=['post_id', 'post_title'])
api_delete_signal = django.dispatch.Signal(providing_args=['post_id', 'post_title'])


@receiver(api_comment_signal)
def api_comment_handler(sender, **kwargs):
    post_id = kwargs.get('post_id')
    post_title = kwargs.get('post_title')
    SiteActivity.objects.create(post_id=post_id, post_title=post_title, task='Comment')

@receiver(api_update_signal)
def api_update_handler(sender, **kwargs):
    post_id = kwargs.get('post_id')
    post_title = kwargs.get('post_title')
    SiteActivity.objects.create(post_id=post_id, post_title=post_title, task='Updated')

@receiver(api_create_signal)
def api_create_handler(sender, **kwargs):
    post_id = kwargs.get('post_id')
    post_title = kwargs.get('post_title')
    SiteActivity.objects.create(post_id=post_id, post_title=post_title, task='Created')

@receiver(api_delete_signal)
def api_delete_handler(sender, **kwargs):
    post_id = kwargs.get('post_id')
    post_title = kwargs.get('post_title')
    SiteActivity.objects.create(post_id=post_id, post_title=post_title, task='Deleted')