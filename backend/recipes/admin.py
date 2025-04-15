from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from .models import (
    Recipe,
    Ingredient,
    IngredientInRecipe,
    Favorite,
    ShoppingCart,
    User,
    Subscription
)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админка для модели ингредиентов"""

    list_display = ('name', 'measurement_unit')
    list_filter = ('measurement_unit',)
    search_fields = ('name', 'measurement_unit')
    ordering = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админка для модели рецептов"""

    list_display = (
        'id',
        'name',
        'cooking_time',
        'author',
        'get_favorites_count',
        'get_ingredients',
        'get_image'
    )
    search_fields = ('name', 'author__username', 'author__email')
    list_filter = ('author', 'created_at')
    ordering = ('id',)

    @admin.display(description='В избранном')
    def get_favorites_count(self, recipe):
        """Отображает общее число добавлений рецепта в избранное"""
        return recipe.favorites.count()

    @admin.display(description='Ингредиенты')
    def get_ingredients(self, recipe):
        """Отображает список ингредиентов рецепта"""
        ingredients = recipe.ingredients.all()
        return mark_safe('<br>'.join([f'{ing.name} - {ing.amount} {ing.measurement_unit}' for ing in ingredients]))

    @admin.display(description='Изображение')
    def get_image(self, recipe):
        """Отображает изображение рецепта"""
        if recipe.image:
            return mark_safe(f'<img src="{recipe.image.url}" width="50" height="50">')
        return 'Нет изображения'


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    """Админка для промежуточной модели ингредиентов в рецепте"""

    list_display = ('recipe', 'ingredient', 'amount')
    search_fields = ('recipe__name', 'ingredient__name')


@admin.register(Favorite, ShoppingCart)
class FavoriteAndShoppingCartAdmin(admin.ModelAdmin):
    """Админка для моделей избранного и списка покупок"""

    list_display = ('user', 'recipe')
    search_fields = ('user__email', 'recipe__name')
    list_filter = ('user',)


@admin.register(User)
class UserAdmin(UserAdmin):
    """Модель пользователей для админ-зоны проекта"""

    list_display = (
        'id',
        'username',
        'get_full_name',
        'email',
        'get_avatar',
        'get_recipes_count',
        'get_subscriptions_count',
        'get_subscribers_count'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('id',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email', 'avatar')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    @admin.display(description='ФИО')
    def get_full_name(self, user):
        """Отображает полное имя пользователя"""
        return f'{user.first_name} {user.last_name}'

    @admin.display(description='Аватар')
    def get_avatar(self, user):
        """Отображает аватар пользователя"""
        if user.avatar:
            return mark_safe(f'<img src="{user.avatar.url}" width="50" height="50">')
        return 'Нет аватара'

    @admin.display(description='Рецепты')
    def get_recipes_count(self, user):
        """Отображает количество рецептов пользователя"""
        return user.recipes.count()

    @admin.display(description='Подписки')
    def get_subscriptions_count(self, user):
        """Отображает количество подписок пользователя"""
        return user.subscriptions.count()

    @admin.display(description='Подписчики')
    def get_subscribers_count(self, user):
        """Отображает количество подписчиков пользователя"""
        return user.subscribers.count()


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Модель подписок для админ-зоны проекта"""

    list_display = ('user', 'author')
    search_fields = ('user__email', 'author__email')
