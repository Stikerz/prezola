from django.urls import path

from wedding_list.views import (
    WeddingListCAPIView,
    WeddingListRUDAPIView,
    ProductAPIView,
    UserAPIView,
    UserDetailView,
    ProductRUDAPIView,
)

urlpatterns = [
    path("users/", UserAPIView.as_view(), name="user_list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("products/", ProductAPIView.as_view(), name="product_list"),
    path("product/<int:pk>/", ProductRUDAPIView.as_view(), name="product_detail"),
    path("list/", WeddingListCAPIView.as_view(), name="wedding_list"),
    path("listitem/<int:pk>/", WeddingListRUDAPIView.as_view(), name="wedding_item"),
]
