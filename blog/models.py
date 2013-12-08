from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField

class Post(models.Model):
    """Basic model for blog posts, includes comments and tags as lists.
    
    """
    title = models.CharField(max_length=255)
    permalink = models.CharField(max_length=255)
    text = models.TextField()
    tags = ListField()
    comments = ListField( EmbeddedModelField( 'Comment' ) )
    created_on = models.DateTimeField( auto_now_add=True, null=True )
    updated_on = models.DateTimeField( null=True )
    
    def __unicode__(self):
        return '%s - %s ...' % ( self.title, self.text[:30] )
    
class Comment(models.Model):
    """Comment model, to be included as a list in the Post model.
    
    """
    author = EmbeddedModelField( 'Author' )
    text = models.TextField()
    created_on = models.DateTimeField( auto_now_add=True )

    def __unicode__(self):
        return '%s: %s' % (self.author.name, self.text[:50] )
    
class Author(models.Model):
    """Author model used in Comments
    
    """
    name = models.CharField(max_length=255)
    email = models.EmailField()
    