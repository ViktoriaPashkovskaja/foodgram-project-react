from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']
    email = models.EmailField(
        verbose_name='Email',
        unique=True
    )

    class Meta:
        ordering = ['date_joined']

    def __str__(self):
        return self.username


class Follow(models.Model):
    objects = None
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed_to',
        verbose_name='follow')
    subscribed_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Who is subscribed to')

    class Meta:
        verbose_name = 'subscriber'
        verbose_name_plural = 'subscribers'
        unique_together = ('subscriber', 'subscribed_to',)
