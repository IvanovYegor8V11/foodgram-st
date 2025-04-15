from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    Recipe,
    Ingredient,
    IngredientInRecipe,
    Favorite,
    ShoppingCart
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
