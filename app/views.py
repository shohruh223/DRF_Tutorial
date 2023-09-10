from rest_framework.viewsets import ModelViewSet
from app.models import Product
from app.serializer import ProductModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["title", "price"]
    search_fields = ["title", "price"]
    ordering_fields = ["title", "price"]
