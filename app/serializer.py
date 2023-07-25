from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from app.models import Product


class ProductModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username


        return token