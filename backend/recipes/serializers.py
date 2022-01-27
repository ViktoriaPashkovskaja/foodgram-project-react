from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from django.db.models import F
from rest_framework import serializers
from users.serializers import CustomUserSerializer
from rest_framework.serializers import ValidationError

from .models import (Favorites, IngredientAmount, Recipe, Ingredient,
                     ShoppingCart, Tag)

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientListSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement = serializers.CharField(
        source='ingredient.measurement', read_only=True)
    amount = serializers.IntegerField()


class IngredientsAmountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    ingredients = IngredientListSerializer(
        source='ingredients_amount', many=True)
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    is_favorites = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_favorites(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorites.objects.filter(
            recipe_id=obj, user_id=request.user).exists()

    def get_is_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(recipe_id=obj,
                                           user_id=request.user).exists()

    class Meta:
        model = Recipe
        fields = ('__all__')


class RecipeCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientsAmountSerializer(
        source='ingredients_amount', many=True)
    name = serializers.CharField(required=False)
    text = serializers.CharField(required=False)

    class Meta:
        model = Recipe
        fields = ('__all__')

    def validate_ingredients(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise ValidationError('Необходимо выбрать ингредиент!')
        for ingredient in ingredients:
            if int(ingredient['amount']) <= 0:
                raise ValidationError('Количество больше нуля')
        return data

    @staticmethod
    def validate_cooking_time(data):
        if data <= 0:
            raise ValidationError('Время приготовления больше нуля')
        return data

    def create(self, validated_data):
        validated_data.pop('ingredients_amount')
        tags = validated_data.pop('tags')
        recipe = super().create(validated_data)
        ingredients_amount = self.get_ingredients_list(
            self.initial_data['ingredients'], recipe)
        recipe.tags.set(tags)
        recipe.ingredients_amount.set(ingredients_amount)
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        instance.image = validated_data.get('image', instance.image)
        ingredients_data = validated_data.pop('ingredients_amount', None)
        tags_data = validated_data.pop('tags', None)
        if tags_data:
            instance.tags.set(tags_data)
        if ingredients_data:
            ingredient = self.initial_data['ingredients']
            ingredients = self.get_ingredients_list(
                ingredient,
                instance)
            instance.ingredients_amount.set(ingredients)
        instance.save()
        return instance

    @staticmethod
    def get_ingredients_list(ingredients, recipe):
        ingredients_list = []
        ingredients_to_delete = IngredientAmount.objects.filter(
            recipe_id=recipe)
        if ingredients_to_delete:
            for ingredient in ingredients_to_delete:
                ingredient.delete()
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            ingredient_instance = Ingredient.objects.get(id=ingredient_id)
            if IngredientAmount.objects.filter(
                    recipe_id=recipe,
                    ingred_id=ingredient_id).exists():
                amount += F('amount')
            ingredient, updated = IngredientAmount.objects.update_or_create(
                recipe_id=recipe, ingred=ingredient_instance,
                defaults={'amount': amount})
            ingredients_list.append(ingredient)
        return ingredients_list


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement',)


class ShoppingCartSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='recipe_id.name')
    image = Base64ImageField(source='recipe_id.image')
    cooking_time = serializers.ReadOnlyField(source='recipe_id.cooking_time')

    class Meta:
        model = ShoppingCart
        fields = ('user_id', 'recipe_id')
