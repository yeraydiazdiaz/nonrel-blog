from django.db import models
from django.utils import timezone
from djangotoolbox.fields import ListField, EmbeddedModelField


class Post(models.Model):
    """
    Basic model for blog posts, includes comments and tags as lists.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    permalink = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.IntegerField()
    text = models.TextField()
    tags = ListField(blank=True, null=True)
    comments = ListField(EmbeddedModelField('Comment'), blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    def create_permalink_from_title(self):
        """
        Create a permalink based on filtering words and whitespaces into underscores.
        """
        import re
        exp = re.compile('\W')
        whitespace = re.compile('\s')
        temp_title = whitespace.sub("_",self.title)
        self.permalink = exp.sub('', temp_title)
    
    def save(self, *args, **kwargs):
        self.create_permalink_from_title() 
        super(Post, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return '%s - %s ...' % (self.title, self.text[:30].replace('\n', ''))


class Comment(models.Model):
    """
    Comment model, to be included as a list in the Post model.
    """
    author = EmbeddedModelField('Author')
    text = models.TextField()
    created_on = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __unicode__(self):
        return u'%s: %s' % (self.author.name, self.text[:50] )


class Author(models.Model):
    """
    Author model used in Comments
    """
    name = models.CharField(max_length=255)
    email = models.EmailField()


class SiteActivity(models.Model):
    """
    Information about a certain activity in the site, used in combination with signals.
    """
    user_id = models.IntegerField(blank=True, null=True)
    post_id = models.IntegerField(blank=True, null=True)
    post_title = models.CharField(max_length=255, blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now)

    TASK_CHOICES = (
        ('Created', 'Created a post'),
        ('Updated', 'Updated a post'),
        ('Deleted', 'Deleted a post'),
        ('Comment', 'Commented a post'),
    )
    
    task = models.CharField(max_length=30, choices=TASK_CHOICES, default='Updated')

    def __unicode__(self):
        return u'%s activity on post: %s' % (self.task, self.post_title)
