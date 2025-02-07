from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db.models import Count, Q
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
    list_display = ('name', 'measurement_unit', 'recipe_count')
    list_filter = ('measurement_unit',)
    search_fields = ('name', 'measurement_unit')
    ordering = ('name',)

    @admin.display(description='Число рецептов')
    def recipe_count(self, obj):
        """Отображает количество рецептов, в которых используется ингредиент."""
        return obj.recipes.count()


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админка для модели рецептов"""
    list_display = (
        'id',
        'name',
        'cooking_time',
        'author',
        'get_favorites_count',
        'display_products',
        'display_image'
    )
    search_fields = ('name', 'author__username', 'author__email')
    list_filter = ('author', 'created_at', 'cooking_time_category')
    ordering = ('id',)

    @admin.display(description='В избранном')
    def get_favorites_count(self, recipe):
        """Отображает общее число добавлений рецепта в избранное."""
        return recipe.favorites.count()

    @admin.display(description='Продукты')
    @mark_safe
    def display_products(self, recipe):
        """Отображает список продуктов в HTML-формате."""
        products = recipe.ingredients.values_list('name', flat=True)
        return '<br>'.join(products)

    @admin.display(description='Картинка')
    @mark_safe
    def display_image(self, recipe):
        """Отображает миниатюру изображения рецепта."""
        if recipe.image:
            return f'<img src="{recipe.image.url}" width="50" height="50" />'
        return "Нет изображения"

    def get_queryset(self, request):
        """Добавляем аннотацию для подсчета числа рецептов в каждой категории времени готовки."""
        queryset = super().get_queryset(request)
        # Вычисляем пороги N и M (25% и 75% квартили)
        cooking_times = queryset.values_list('cooking_time', flat=True).order_by('cooking_time')
        n = len(cooking_times)
        if n > 0:
            q25 = cooking_times[n // 4] if n >= 4 else cooking_times[0]
            q75 = cooking_times[3 * n // 4] if n >= 4 else cooking_times[-1]
        else:
            q25, q75 = 0, 0

        # Аннотируем категории времени готовки
        queryset = queryset.annotate(
            cooking_time_category=models.Case(
                models.When(cooking_time__lte=q25, then=models.Value(f'быстрее {q25} мин')),
                models.When(cooking_time__lte=q75, then=models.Value(f'быстрее {q75} мин')),
                default=models.Value('долго'),
                output_field=models.CharField(),
            )
        )
        return queryset

    def cooking_time_category(self, obj):
        """Возвращает категорию времени готовки для фильтра."""
        return obj.cooking_time_category

    class CookingTimeFilter(admin.SimpleListFilter):
        """Фильтр по времени готовки."""
        title = 'время готовки'
        parameter_name = 'cooking_time_category'

        def lookups(self, request, model_admin):
            """Определяет варианты фильтрации."""
            queryset = model_admin.get_queryset(request)
            categories = queryset.values('cooking_time_category').annotate(count=Count('id'))
            return [
                (cat['cooking_time_category'], f"{cat['cooking_time_category']} ({cat['count']})")
                for cat in categories
            ]

        def queryset(self, request, queryset):
            """Фильтрует рецепты по выбранной категории."""
            if self.value():
                return queryset.filter(cooking_time_category=self.value())
            return queryset

    list_filter += (CookingTimeFilter,)


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