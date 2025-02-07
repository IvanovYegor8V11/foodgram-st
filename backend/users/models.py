from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Модель пользователей"""
    email = models.EmailField(
        _('email address'),  # Локализация
        unique=True,
        max_length=254
    )
    username = models.CharField(
        _('username'),  # Локализация
        max_length=150,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message=_('Username должен содержать только буквы, '
                      'цифры и следующие символы: @ . + -')
        )]
    )
    first_name = models.CharField(
        _('first name'),  # Локализация
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        _('last name'),  # Локализация
        max_length=150,
        blank=True,
    )
    avatar = models.ImageField(
        _('avatar'),  # Локализация
        upload_to='avatars/',
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'password'
    ]

    class Meta:
        verbose_name = _('user')  # Локализация
        verbose_name_plural = _('users')  # Локализация
        ordering = ('email',)

    def __str__(self):
        return self.email


User = get_user_model()


class Subscription(models.Model):
    """Модель подписок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',  # Исправлено на более логичное название
        verbose_name=_('subscriber')  # Локализация
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',  # Исправлено на более логичное название
        verbose_name=_('author')  # Локализация
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]
        verbose_name = _('subscription')  # Локализация
        verbose_name_plural = _('subscriptions')  # Локализация

    def __str__(self):
        return f'{self.user} подписан на {self.author}'