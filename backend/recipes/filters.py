from django.contrib.auth import get_user_model
from django_filters import FilterSet, filters
from rest_framework.filters import SearchFilter

from .models import Recipe, Tag

User = get_user_model()


class RecipeFilterSet(FilterSet):
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug')
    favourites = filters.BooleanFilter(
        label="Favorites",
        method='filter_is_favorites')
    shopping_cart = filters.BooleanFilter(
        label="Is in shopping cart",
        method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'favourites', 'shopping_cart']

    def filter_is_favorites(self, queryset, value):
        if value:
            return queryset.filter(favorites__user_id=self.request.user)
        return queryset.all()

    def filter_is_shopping_cart(self, queryset, value):
        if value:
            return queryset.filter(buy__user_id=self.request.user)
        return queryset.all()


class SearchFilter(SearchFilter):
    search_param = "name"
