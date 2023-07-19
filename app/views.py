from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import Product
from app.serializers import ProductModelSerializer


class ProductView(APIView):
    def get(self, request, product_id=None):
        if product_id:
            try:
                product = Product.objects.filter(id=product_id).first()
                serializer = ProductModelSerializer(product)
                return Response(data=serializer.data,
                                status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response(data={"errors":"This product is not found"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            products = Product.objects.all()
            serializer = ProductModelSerializer(instance=products,
                                                many=True)
            return Response(data=serializer.data,
                            status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        try:
            product = Product.objects.filter(id=product_id).first()
        except Product.DoesNotExist:
            return Response(data={"errors":"This product is not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = ProductModelSerializer(instance=product,
                                            data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_200_OK)
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        try:
            product = Product.objects.filter(id=product_id).first()
        except Product.DoesNotExist:
            return Response(data={"errors":"This product is not found"},
                            status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(data={"message":"This product is successfully deleted"},
                        status=status.HTTP_204_NO_CONTENT)
