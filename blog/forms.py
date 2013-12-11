"""
    Forms definition for blog app.
"""

from django import forms
from django.forms import ModelForm
from django.contrib.formtools.preview import FormPreview
from django.http import HttpResponseRedirect
from blog.models import *

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = [ 'text' ]
        labels = { 'text': 'Comment' }
        widgets = { 
                  'text': forms.Textarea( 
                                         attrs={'cols': 80,
                                                'rows': 20,
                                                'placeholder': 'Your comment here...'
                                                } 
                                         ) 
                 }

class AuthorForm(forms.ModelForm):
    
    class Meta:
        model = Author
        fields = [ 'name', 'email' ]
        labels = { 
                  'name': 'Your name',
                  'email': 'Your email'
                }

class PostForm(forms.ModelForm):
    
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

# Form previews
class CommentFormPreview( FormPreview ):
    
    def done(self, request, cleaned_data):
        return HttpResponseRedirect( '/comment/success' )