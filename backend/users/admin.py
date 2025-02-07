from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Subscription, User

@admin.register(User)
class UserAdmin(UserAdmin):
    """Модель пользователей для админ-зоны проекта"""
    list_display = (
        'id',
        'username',
        'email',
        'full_name',
        'avatar_preview',
        'recipe_count',
        'subscription_count',
        'subscriber_count',
    )
    search_fields = ('username', 'email')
    ordering = ('id',)

    @admin.display(description="ФИО")
    def full_name(self, obj):
        """Отображение полного имени пользователя (имя + фамилия)."""
        return f"{obj.first_name} {obj.last_name}".strip()

    @admin.display(description="Аватар")
    @mark_safe
    def avatar_preview(self, obj):
        """Отображение аватара пользователя."""
        if obj.avatar:
            return f'<img src="{obj.avatar.url}" width="50" height="50" />'
        return "Нет аватара"

    @admin.display(description="Рецепты")
    def recipe_count(self, obj):
        """Количество рецептов пользователя."""
        return obj.recipes.count()

    @admin.display(description="Подписки")
    def subscription_count(self, obj):
        """Количество подписок пользователя."""
        return obj.subscriptions.count()

    @admin.display(description="Подписчики")
    def subscriber_count(self, obj):
        """Количество подписчиков пользователя."""
        return obj.subscribers.count()


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Модель подписок для админ-зоны проекта"""
    list_display = ('user', 'author')
    search_fields = ('user__email', 'author__email')