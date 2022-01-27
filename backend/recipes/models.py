from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models import (CASCADE, CharField, ForeignKey, ImageField,
                              ManyToManyField, Model, PositiveIntegerField,
                              SlugField, TextField, UniqueConstraint)

User = get_user_model()

COOKING_TIME_MIN_ERROR = (
    'Время приготовления не может быть меньше одной минуты!'
)
INGREDIENT_MIN_AMOUNT_ERROR = (
    'Количество ингредиентов не может быть меньше {min_value}!'
)


class Ingredient(Model):
    name = CharField('Name', max_length=200)
    measurement_unit = CharField('Measurement_unit', max_length=200)

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


class Tag(Model):
    name = CharField('Name', max_length=200, unique=True)
    color = CharField('Color in HEX', max_length=7, unique=True)
    slug = SlugField('Slug', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return f'{self.name}'


class Recipe(Model):
    name = CharField('Name', max_length=200)
    text = TextField('Description')
    ingredients = ManyToManyField(
        Ingredient,
        through='CountOfIngredient',
        verbose_name='Ingredients'
    )
    tags = ManyToManyField(
        Tag,
        verbose_name='Tags'
    )
    image = ImageField('Image', upload_to='recipes/')

    cooking_time = PositiveIntegerField(
        'Время приготовления',
        validators=(MinValueValidator(
            1,
            message=COOKING_TIME_MIN_ERROR,
        ),)
    )
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='recipes',
        verbose_name='Author',
    )

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.name})'


class CountOfIngredient(Model):
    ingredient = ForeignKey(
        Ingredient,
        on_delete=CASCADE,
        verbose_name='Ingredient',
    )
    amount = PositiveIntegerField(
        'Количество',
        validators=(MinValueValidator(
            1,
            message=INGREDIENT_MIN_AMOUNT_ERROR.format(
                min_value=1
            )
        ),)
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        verbose_name='Recipe',
    )

    class Meta:
        verbose_name = 'Ingredient Quantity'
        verbose_name_plural = 'Ingredients Quantity'
        constraints = (
            UniqueConstraint(
                fields=('ingredient', 'recipe',),
                name='unique_ingredient_amount',
            ),
        )


class ShoppingCart(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='shopping_cart',
        verbose_name='User',
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='shopping_cart',
        verbose_name='Recipes',
    )

    class Meta:
        verbose_name = 'Shopping list'
        verbose_name_plural = 'Shopping list'
        constraints = (
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart',
            ),
        )


class Favorite(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='favorites',
        verbose_name='User',
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='favorites',
        verbose_name='Recipe',
    )

    class Meta:
        verbose_name = 'Favourites'
        verbose_name_plural = 'Favourites'
        constraints = (
            UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_user_recipe',
            ),
        )
