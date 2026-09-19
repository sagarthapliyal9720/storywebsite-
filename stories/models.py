from django.db import models
from django.contrib.auth.models import User


class Story(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stories"
    )
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('ready', 'Ready'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    title = models.CharField(max_length=200)

    content = models.TextField()

    language = models.CharField(max_length=20)

    genre = models.CharField(max_length=50)

    audio = models.URLField(
    blank=True,
    null=True
)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "story")  # ek user ek story ko ek hi baar like kare


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="bookmarks")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "story")