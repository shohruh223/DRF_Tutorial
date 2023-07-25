from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from app.models import Product
from app.serializer import ProductModelSerializer


class ProductView(ModelViewSet):
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated,]
    parser_classes = [MultiPartParser,]

