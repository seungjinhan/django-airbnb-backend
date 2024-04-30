from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.viewsets import ModelViewSet

from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(
        kind=Category.CategoryKindChoices.ROOMS,
    )


# class Categories(APIView):

#     def get(self, req):
#         all = Category.objects.all()
#         srz = CategorySerializer(all, many=True)
#         return Response(srz.data)

#     def post(self, req):
#         srz = CategorySerializer(data=req.data)
#         if srz.is_valid():
#             new_data = srz.save()
#             return Response(CategorySerializer(new_data).data)
#         else:
#             return Response(srz.error)


# class CategoryDetail(APIView):

#     def get_category(self, pk):
#         try:
#             return Category.objects.get(pk=pk)
#         except Category.DoesNotExist:
#             raise NotFound

#     def get(self, req, pk):
#         category = self.get_category(pk)
#         return Response(CategorySerializer(category).data)

#     def put(self, req, pk):
#         category = self.get_category(pk)
#         serializer = CategorySerializer(
#             category,
#             data=req.data,
#             partial=True,
#         )
#         if serializer.is_valid():
#             update_date = serializer.save()
#             return Response(CategorySerializer(update_date).data)
#         else:
#             return Response(serializer.errors)

#     def delete(self, req, pk):
#         category = self.get_category(pk)
#         category.delete()
#         return Response(status=HTTP_204_NO_CONTENT)


# @api_view(["GET", "POST"])
# def categories(req):
#     if req.method == "GET":
#         all = Category.objects.all()
#         srz = CategorySerializer(all, many=True)
#         return Response(srz.data)
#     elif req.method == "POST":
#         srz = CategorySerializer(data=req.data)
#         if srz.is_valid():
#             new_data = srz.save()
#             return Response(CategorySerializer(new_data).data)
#         else:
#             return Response(srz.error)


# @api_view(["GET", "PUT", "DELETE"])
# def category(req, pk):
#     try:
#         category = Category.objects.get(pk=pk)
#     except Category.DoesNotExist:
#         raise NotFound

#     if req.method == "GET":
#         return Response(CategorySerializer(category).data)
#     elif req.method == "PUT":
#         serializer = CategorySerializer(
#             category,
#             data=req.data,
#             partial=True,
#         )
#         if serializer.is_valid():
#             update_date = serializer.save()
#             return Response(CategorySerializer(update_date).data)
#         else:
#             return Response(serializer.errors)
#     elif req.method == "DELETE":
#         category.delete()
#         return Response(status=HTTP_204_NO_CONTENT)
