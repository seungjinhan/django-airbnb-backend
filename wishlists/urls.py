from django.urls import path
from .views import WishListView, WishListDetail, WishListToggle

urlpatterns = [
    path("", WishListView.as_view()),
    path("<int:pk>", WishListDetail.as_view()),
    path("<int:pk>/rooms/<int:room_pk>", WishListToggle.as_view()),
]
