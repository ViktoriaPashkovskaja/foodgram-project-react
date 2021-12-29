# Generated by Django 3.2.7 on 2021-12-29 15:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'Ingredient', 'verbose_name_plural': 'Ingredients'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Recipe', 'verbose_name_plural': 'Recipes'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'verbose_name': 'ShoppingCart', 'verbose_name_plural': 'ShoppingCart'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Tag', 'verbose_name_plural': 'Tags'},
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='measurement_unit',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='measurement',
            field=models.CharField(default='', max_length=200, verbose_name='Unit of measurement'),
        ),
        migrations.AddField(
            model_name='ingredientamount',
            name='ingredient',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_amount', to='recipes.ingredient', verbose_name='Ingredients'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='ingredientamount',
            name='amount',
            field=models.PositiveIntegerField(verbose_name='Quantity'),
        ),
        migrations.AlterField(
            model_name='ingredientamount',
            name='recipe_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_amount', to='recipes.recipe', verbose_name='Recipe'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(to='recipes.Ingredient', verbose_name='Ingredients'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='date of publication of the recipe'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipe_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buy', to='recipes.recipe', verbose_name='Recipe'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buy', to=settings.AUTH_USER_MODEL, verbose_name='ShoppingCart'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Tag name'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, verbose_name='slug'),
        ),
        migrations.AlterUniqueTogether(
            name='ingredientamount',
            unique_together={('ingredient', 'recipe_id')},
        ),
        migrations.DeleteModel(
            name='Favorite',
        ),
        migrations.AddField(
            model_name='favorites',
            name='recipe_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='recipes.recipe', verbose_name='Recipe'),
        ),
        migrations.AddField(
            model_name='favorites',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.RemoveField(
            model_name='ingredientamount',
            name='ingred',
        ),
        migrations.AlterUniqueTogether(
            name='favorites',
            unique_together={('user_id', 'recipe_id')},
        ),
    ]
