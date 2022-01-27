from django.contrib.auth.models import AbstractUser
from django.db.models import (CASCADE, CharField, EmailField, ForeignKey,
                              Model, UniqueConstraint)


class User(AbstractUser):
    email = EmailField('Email', max_length=254, unique=True)
    username = CharField('Username', max_length=150, unique=True, blank=True)
    first_name = CharField('Name', max_length=150)
    last_name = CharField('Surname', max_length=150)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class Subscribe(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='subscriber',
        verbose_name='Subscriber'
    )
    following = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='following',
        verbose_name='Author'
    )

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        constraints = (
            UniqueConstraint(
                fields=('user', 'following',),
                name='unique_subscribe',
            ),
        )
