"""
    Forms definition for blog app.
"""

from django import forms
from django.forms import ModelForm
from django.contrib.formtools.preview import FormPreview
from django.http import HttpResponseRedirect
from blog.models import *
from django.forms.util import ErrorList

class CommentForm(forms.ModelForm):
    """ModelForm for Comment.
    """
    class Meta:
        model = Comment
        fields = [ 'text' ]
        labels = { 'text': 'Comment' }
        widgets = { 
                  'text': forms.Textarea( 
                                         attrs={'cols': 80,
                                                'rows': 10,
                                                'placeholder': 'Your comment ...'
                                                } 
                                         ) 
                 }

class AuthorForm(forms.ModelForm):
    """ModelForm for Author.
    """
    class Meta:
        model = Author
        fields = [ 'name', 'email' ]
        labels = { 
                  'name': 'Your name',
                  'email': 'Your email'
                }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'you@example.org'}),
        }
        
class PostForm(forms.ModelForm):
    """ModelForm for Post.
    """
    class Meta:
        model = Post
        fields = [ 'title', 'text' ]
        labels = { 
                  'title': 'Post title',
                  'text': 'Content'
                }
        widgets = {
                   'text': forms.Textarea( 
                                         attrs={'cols': 80,
                                                'rows': 20,
                                                'placeholder': 'Your post here...'
                                                } 
                                         )
                }
        
class BlogErrorList( ErrorList ):
    """Custom error list class.
    """
    def __unicode__(self):
        return self.as_divs()
    
    def as_divs(self):
        if not self:
            return u''
        return u'<div class="alert alert-danger alert-dismissable">\
            <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>\
            <ul class="list-group">%s</ul>\
            </div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])