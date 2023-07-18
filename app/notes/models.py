import uuid

from django.db import models

from app.settings import AUTH_USER_MODEL


class Tag(models.Model):
    """
    Model for saving tags to the Notes
    """

    title = models.CharField(max_length=128)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Note(models.Model):
    """
    Model for saving Notes written by Authors
    """

    title = models.CharField(max_length=128)
    body = models.TextField()
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notes")
    tags = models.ManyToManyField(Tag, related_name="notes", blank=True)
    is_public = models.BooleanField(default=False)
