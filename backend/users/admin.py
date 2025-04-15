from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.db.models import Count
from .models import Subscription, User

@admin.register(User)
class UserAdmin(UserAdmin):
    """Модель пользователей для админ-зоны проекта"""

    def get_full_name_display(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name_display.short_description = 'ФИО'

    def get_avatar_display(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="50" height="50" />')
        return 'Нет аватара'
    get_avatar_display.short_description = 'Аватар'

    def get_recipe_count(self, obj):
        return obj.recipes.count()
    get_recipe_count.short_description = 'Рецептов'

    def get_subscriptions_count(self, obj):
        return obj.users.count()
    get_subscriptions_count.short_description = 'Подписок'

    def get_subscribers_count(self, obj):
        return obj.authors.count()
    get_subscribers_count.short_description = 'Подписчиков'

    list_display = (
        'id',
        'username',
        'get_full_name_display',
        'email',
        'get_avatar_display',
        'get_recipe_count',
        'get_subscriptions_count',
        'get_subscribers_count',
    )
    search_fields = ('username', 'email')
    ordering = ('id',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Модель подписок для админ-зоны проекта"""

    list_display = ('user', 'author')
    search_fields = ('user__email', 'author__email')
