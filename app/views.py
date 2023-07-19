from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, \
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from app.models import Product
from app.serializer import ProductModelSerializer


# class ProductCreateAPIView(CreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductModelSerializer
#
#
# class ProductListAPIView(ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductModelSerializer


# class ProductListCreateAPIView(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductModelSerializer


# class ProductRetrieveAPIView(RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductModelSerializer
#
#
# class ProductUpdateAPIView(UpdateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductModelSerializer
#
#
# class ProductDestroyAPIView(DestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductModelSerializer


# class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductModelSerializer


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer


