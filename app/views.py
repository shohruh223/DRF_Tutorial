from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import Product
from app.serializers import ProductModelSerializer


class ProductListView(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductModelSerializer(instance=products, many=True)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)


class ProductCreateView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type="object",
            properties={
                "title": openapi.Schema(type="string"),
                "description": openapi.Schema(type="string"),
                "price": openapi.Schema(type="integer"),
            },
            required=["title", "price"]
        ),
        responses={
            201: "Product created successfully",
            400: "Invalid data provided"
        }
    )
    def post(self, request):
        serializer = ProductModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class ProductGetView(APIView):

    def get(self, request, product_id):
        if product_id:
            product = Product.objects.filter(id=product_id).first()
            serializer = ProductModelSerializer(product)
            return Response(data=serializer.data,
                            status=status.HTTP_200_OK)
        return Response(data={"errors":"This product is not found"},
                        status=status.HTTP_404_NOT_FOUND)


class ProductEditView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('product_id', openapi.IN_PATH, description="ID of the product to edit",
                              type=openapi.TYPE_INTEGER),
        ],
        request_body=openapi.Schema(
            type="object",
            properties={
                "title": openapi.Schema(type="string"),
                "description": openapi.Schema(type="string"),
                "price": openapi.Schema(type="integer"),
            },
        ),
        responses={
            200: "Product updated successfully",
            400: "Invalid data provided",
            404: "Product not found"
        }
    )
    def put(self, request, product_id):
        try:
            product = Product.objects.filter(id=product_id).first()
        except Product.DoesNotExist:
            return Response(data={"errors": "This product is not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = ProductModelSerializer(instance=product,
                                            data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_200_OK)
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class ProductDeleteView(APIView):

    def delete(self, request, product_id):
        try:
            product = Product.objects.filter(id=product_id).first()
        except Product.DoesNotExist:
            return Response(data={"errors":"This product is not found"},
                            status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(data={"message":"This product is successfully deleted"},
                        status=status.HTTP_204_NO_CONTENT)
