from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from wedding_list.models import Product, WeddingList
from wedding_list.serializers import (
    ProductSerializer,
    WeddingListSerializer,
    UserSerializer,
)
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters


class UserAPIView(ListCreateAPIView):
    """view for listing a queryset or creating a model instance."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []


class UserDetailView(RetrieveUpdateDestroyAPIView):
    """view for retrieving, updating or deleting a model instance."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class ProductAPIView(ListCreateAPIView):
    """view for listing a queryset & creating instance"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class ProductRUDAPIView(RetrieveUpdateDestroyAPIView):
    """view for listing a queryset & creating instance"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class WeddingListCAPIView(ListCreateAPIView):
    queryset = WeddingList.objects.all()
    serializer_class = WeddingListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["product__id"]

    def get_queryset(self):
        queryset = WeddingList.objects.all().filter(user=self.request.user.id)
        return queryset


class WeddingListRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = WeddingList.objects.all()
    serializer_class = WeddingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = WeddingList.objects.all().filter(user=self.request.user.id)
        return queryset


class CustomAuthToken(ObtainAuthToken):  # pragma: no cover
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
            }
        )
