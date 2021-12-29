import io

from .permissions import Author, ReadOnly
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.serializers import RecipeSerializer as FavoriteRecipeSerializer
from django_filters import rest_framework as filters

from .filters import SearchFilter, RecipeFilterSet
from .models import (Favorites, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)
from .serializers import (IngredientListSerializer, IngredientSerializer,
                          RecipeListSerializer, ShoppingCartSerializer,
                          TagSerializer, RecipeCreateSerializer)


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilterSet

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['GET'])
    def shopping_cart(self, request, pk=None):
        in_purchases = ShoppingCart.objects.filter(
            recipe_id=int(pk),
            user_id=request.user
        )
        if in_purchases.exists():
            raise ValidationError('Рецепт уже есть в корзине')
        recipe = Recipe.objects.get(id=int(pk))
        purchases = ShoppingCart.objects.create(
            recipe_id=recipe,
            user_id=self.request.user
        )
        purchases.save()
        serializer = ShoppingCartSerializer(purchases)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, pk=None):
        in_purchases = get_object_or_404(
            ShoppingCart,
            recipe_id=int(pk),
            user_id=self.request.user)
        in_purchases.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def favorites(self, request, pk=None):
        user = request.user
        in_favorites = Favorites.objects.filter(
            user_id=user.id,
            recipe_id=pk)
        if in_favorites:
            raise ValidationError(
                detail='Рецепт уже находится в избранном')
        recipe = get_object_or_404(Recipe, id=int(pk))
        favorites = Favorites.objects.create(
            user_id=user,
            recipe_id=recipe)
        favorites.save()
        serializer = FavoriteRecipeSerializer(recipe)
        return Response(serializer.data)

    @favorites.mapping.delete
    def delete_favorite(self, pk=None):
        user = self.request.user
        in_favorites = get_object_or_404(
            Favorites,
            user_id=user.id,
            recipe_id=pk
        )
        in_favorites.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self):
        queryset = ShoppingCart.objects.filter(
            user_id=self.request.user).values(
            'recipe_id__ingredients_amount__ingredient__name',
            'recipe_id__ingredients_amount__ingredient__measurement').annotate(
                Sum('recipe_id__ingredients_amount__amount'))
        buffer = get_pdf_file(queryset)
        return FileResponse(buffer, as_attachment=True, filename='list.pdf')

    def get_permissions(self):
        if self.action in ['shopping_cart', 'favorite',
                           'download_shopping_cart']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [Author | ReadOnly]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return RecipeCreateSerializer
        return RecipeListSerializer


class IngredientsAmountView(generics.ListAPIView):
    queryset = IngredientAmount.objects.all()
    serializer_class = IngredientListSerializer


class IngredientsViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ['^name']
    pagination_class = None


def get_pdf_file(queryset):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setLineWidth(.3)
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    p.setFont('FreeSans', 14)
    t = p.beginText(30, 750, direction=0)
    t.textLine('Список покупок')
    p.line(30, 747, 580, 747)
    t.textLine(' ')
    for qs in queryset:
        title = qs['recipe_id__ingredients_amount__ingredient__name']
        amount = qs['recipe_id__ingredients_amount__amount__sum']
        mu = qs['recipe_id__ingredients_amount__ingredient__measurement']
        t.textLine(f'{title} ({mu}) - {amount}')
    p.drawText(t)
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
