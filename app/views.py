from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet
from app.models import Product
from app.serializer import ProductModelSerializer


class ProductView(ModelViewSet):
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()
    parser_classes = (MultiPartParser, FormParser)


