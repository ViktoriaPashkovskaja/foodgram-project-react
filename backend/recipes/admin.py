from django.contrib import admin

from .models import (Favorites, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement', 'id')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'added_in_favorites')
    list_filter = ('name', 'author', 'tags',)
    readonly_fields = ('added_in_favorites',)

    def added_in_favorites(self, obj):
        return obj.favorites.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color',)


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'amount')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'recipe_id')


@admin.register(Favorites)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'recipe_id')
    list_filter = ('user_id', 'recipe_id')
