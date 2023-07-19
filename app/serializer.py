from rest_framework import serializers

from app.models import Product


class ProductModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ()