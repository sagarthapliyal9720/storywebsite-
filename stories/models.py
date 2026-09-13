from django.db import models
from django.contrib.auth.models import User


class Story(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stories"
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