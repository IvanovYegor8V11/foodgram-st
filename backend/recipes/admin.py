from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.db.models import Count
from .models import (
    User,
    Subscription,
    Recipe,
    Ingredient,
    IngredientInRecipe,
    Favorite,
    ShoppingCart
)


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

    def get_ingredients_display(self, obj):
        ingredients = obj.recipe_ingredients.all()
        return mark_safe('<br>'.join([
            f'{ing.ingredient.name} - {ing.amount} {ing.ingredient.measurement_unit}'
            for ing in ingredients
        ]))
    get_ingredients_display.short_description = 'Продукты'

    def get_image_display(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return 'Нет изображения'
    get_image_display.short_description = 'Картинка'

    def get_favorites_count(self, obj):
        return obj.favorites.count()
    get_favorites_count.short_description = 'В избранном'

    list_display = (
        'id',
        'name',
        'cooking_time',
        'author',
        'get_favorites_count',
        'get_ingredients_display',
        'get_image_display',
    )
    search_fields = ('name', 'author__username', 'author__email')
    list_filter = ('author', 'created_at')
    ordering = ('id',)


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
