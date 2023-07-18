from rest_framework import serializers
from app.models import Category, Product


class CategoryModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ()


class ProductModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ()