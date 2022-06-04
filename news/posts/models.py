from django.utils import timezone
from django.db import models
from django.forms import IntegerField

class Post(models.Model):
    """
    Abstract model of the post
    The user's rating and favorites are stored in the user himself
    """
    
    article = models.IntegerField(unique=True,primary_key=True)
    title_url = models.CharField(max_length=150)
    title = models.CharField(max_length = 100)
    author = models.CharField(max_length = 100)
    summary = models.TextField(max_length=250)
    content = models.TextField()
    views = models.IntegerField()
    rate = models.IntegerField()
    date_created = models.DateTimeField(default=timezone.now)
