from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from .models import Recipe


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(FilterSet):
    is_favorited = filters.BooleanFilter(
        field_name='get_is_favorited', method='filter'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart', method='filter'
    )
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter(self, queryset, name, value):
        if name == 'is_in_shopping_cart' and value:
            queryset = queryset.filter(
                shopping_cart__user=self.request.user
            )
        if name == 'is_favorited' and value:
            queryset = queryset.filter(
                favorite_recipes__user=self.request.user
            )
        return queryset
