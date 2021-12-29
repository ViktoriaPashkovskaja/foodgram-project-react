from django.contrib import admin

from .models import (Favorites, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement')
    list_filter = (
        ('name', admin.EmptyFieldListFilter),
    )


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = (
        ('author', admin.RelatedOnlyFieldListFilter),
        ('tags', admin.RelatedOnlyFieldListFilter),
        ('name', admin.EmptyFieldListFilter),
    )


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'amount')


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'recipe_id')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'recipe_id')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Favorites, FavoriteAdmin)
