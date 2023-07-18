from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from app.settings import AUTH_USER_MODEL


class Author(AbstractUser):
    """ "
    This is the main user model
    """

    def __str__(self):
        return self.username


@receiver(post_save, sender=AUTH_USER_MODEL)
def author_post_save(sender, instance=None, created=False, **kwargs):
    """
    Add a auth token for every newly created author
    """
    if created:
        Token.objects.create(user=instance)
