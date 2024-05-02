from django.urls import path
from .views import PhotoDetail, GetUploadUrl

urlpatterns = [
    path("phtos/get-url", GetUploadUrl.as_view()),
    path("photos/<int:pk>", PhotoDetail.as_view()),
]
