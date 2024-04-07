from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
    

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DR', _('Draft')
        PUBLISHED = 'PB', _('Published')
    
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)
    publish = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, unique_for_date='publish')
    authot = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    published = PostManager()
    tag = TaggableManager()

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title
    
    # Dinamic url to go to post detail page
    def get_absolute_url(self):
        return reverse('post_detail', args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug
        ])
    


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['created'])]


    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


    
