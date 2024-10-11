from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)

class Tag(models.Model):
    name = models.CharField(max_length=50)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='posts')

    class Meta:
        indexes = [
            models.Index(fields=['author']),
        ]

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['post', 'created_at']),
        ]

# class PostTag(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
#
#     class Meta:
#         indexes = [
#             models.Index(fields=['post', 'tag']),
#         ]