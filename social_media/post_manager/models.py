from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.RESTRICT, null=False, blank=False,
                              related_name='owned_post')
    created_at = models.DateTimeField(default=timezone.now, null=False)
    text = models.TextField()
    users = models.ManyToManyField(
        get_user_model(), related_name='Reposts', blank=True , null = True)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    comment_by = models.ForeignKey(get_user_model(), on_delete=models.RESTRICT, null=False, blank=False,
                                   related_name='owned_comment')
    post = models.ForeignKey(Post, on_delete=models.RESTRICT,
                             null=False, blank=False, related_name='commented_post')
    comment = models.TextField()
    
    
