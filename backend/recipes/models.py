from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name')
    measurement = models.CharField(
        max_length=200,
        verbose_name='Unit of measurement',
        default=""
    )

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.name


class Tag(models.Model):
    objects = None
    name = models.CharField(max_length=200, verbose_name='Tag name')
    color = models.CharField(max_length=8, null=True, blank=True)
    slug = models.SlugField(verbose_name='slug', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, related_name='tags')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='author', related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient,
                                         verbose_name='Ingredients')
    pub_date = models.DateTimeField('date of publication of the recipe',
                                    auto_now_add=True, db_index=True,)
    name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to='images/',
        verbose_name='фото',
        null=True,
        blank=True)
    text = models.CharField(max_length=200)
    cooking_time = models.PositiveIntegerField()

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ingredients',
        related_name='ingredients_amount',
        default=""
    )
    recipe_id = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Recipe',
        related_name='ingredients_amount')
    amount = models.PositiveIntegerField(
        verbose_name='Quantity',
    )

    class Meta:
        unique_together = ('ingredient', 'recipe_id',)


class ShoppingCart(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='buy',
        verbose_name='ShoppingCart',
    )
    recipe_id = models.ForeignKey(
        Recipe,
        related_name='buy',
        verbose_name='Recipe',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'ShoppingCart'
        verbose_name_plural = 'ShoppingCart'


class Favorites(models.Model):
    user_id = models.ForeignKey(
        User,
        related_name='favorites',
        verbose_name='User',
        on_delete=models.CASCADE
    )
    recipe_id = models.ForeignKey(
        Recipe,
        related_name='favorites',
        verbose_name='Recipe',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ('user_id', 'recipe_id',)
