from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from app.models import Product, User
from app.permission import IsAuthorOrReadOnly
from app.serializers import ProductModelSerializer, UserModelSerializer


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthorOrReadOnly]


class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return token.key



