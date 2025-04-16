from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    """Модель пользователей"""

    email = models.EmailField(
        unique = True,
        max_length = 254
    )

    username = models.CharField(
        max_length = 150,
        unique = True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Username должен содержать только буквы, '
                    'цифры и следующие символы: @ . + -'
        )]
    )

    first_name = models.CharField(
        max_length=150,
        blank=True,
    )

    last_name = models.CharField(
        max_length=150,
        blank=True,
    )

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'password'
    ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('email',)

    def __str__(self):
        return self.email


User = get_user_model()


class Subscription(models.Model):
    """Модель подписок"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authors',
        verbose_name='Автор рецептов'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.author}'


class Ingredient(models.Model):
    """Модель ингредиентов"""
    name = models.CharField(
        verbose_name = 'Название',
        max_length = 128
    )

    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length = 64
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_measurement_unit'
            )
        ]
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Recipe(models.Model):
    """Модель рецептов"""

    name = models.CharField(
        verbose_name = 'Название',
        max_length = 256
    )

    text = models.TextField(
        verbose_name = 'Описание'
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        through = 'IngredientInRecipe',
    )

    image = models.ImageField(
        verbose_name = 'Картинка',
        upload_to = 'recipes/images/'
    )

    author = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        verbose_name = 'Автор'
    )

    cooking_time = models.IntegerField(
        verbose_name = 'Время приготовления (в минутах)',
        validators=[
            MinValueValidator(
                1, 'Время приготовления не может быть менее 1 минуты'
            )
        ]
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-created_at',)
        default_related_name = 'recipes'

    def __str__(self):
        return f'ID рецепта: {self.id} | {self.name}'


class IngredientInRecipe(models.Model):
    """Промежуточная модель для связи рецептов с ингредиентами"""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )

    amount = models.IntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(
            1,
            'Количество ингредиента должно быть больше нуля!'
        )]
    )

    class Meta:
        verbose_name = 'Продукт рецепта'
        verbose_name_plural = 'Продукты рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]
        default_related_name = 'recipe_ingredients'

    def __str__(self):
        return (f'{self.ingredient.name} - {self.amount}'
                f'{self.ingredient.measurement_unit}'
                f'для {self.recipe.name}')


class UserOfRecipeBase(models.Model):
    """Базовый класс для Favorite и ShoppingCart"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='%(class)ss'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='%(class)ss'
    )

    '''К сожалению я узнал, что default_related_name в Meta, 
    не поддерживает динамическое указание названия related_name,
    поэтому пришлось оставить related_name в ForeignKey'''

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user.username} -> {self.recipe.name}'


class Favorite(UserOfRecipeBase):
    """Модель избранных рецептов"""

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class ShoppingCart(UserOfRecipeBase):
    """Модель корзины покупок"""

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'
