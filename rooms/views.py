from rest_framework.views import APIView
from django.db import transaction
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer


class Amenities(APIView):

    def get(self, req):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, req):
        serializer = AmenitySerializer(data=req.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, req, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, req, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity, data=req.data, partial=True)
        if serializer.is_valid():
            update_amenity = serializer.save()
            return Response(AmenitySerializer(update_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, req, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    def get(self, req):
        all_data = Room.objects.all()
        serializer = RoomListSerializer(all_data, many=True)
        return Response(serializer.data)

    def post(self, req):
        user = req.user
        if user.is_authenticated:
            serializer = RoomDetailSerializer(data=req.data)
            if serializer.is_valid():
                category_pk = req.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The Category should be rooms")

                except Category.DoesNotExist:
                    raise ParseError("The Category not found")

                try:
                    with transaction.atomic():
                        room = serializer.save(owner=user, category=category)

                        # Amenity 체크
                        amenities = req.data.get("amenities")
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                        serializer = RoomDetailSerializer(room)
                        return Response(serializer.data)
                except Exception:
                    raise ParseError("The Amenity is not found")
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, req, pk):
        data = self.get_object(pk)
        serializer = RoomDetailSerializer(data)
        return Response(serializer.data)

    def put(self, req, pk):
        room = self.get_object(pk)
        if not req.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != req.user:
            raise PermissionDenied

    def delete(self, req, pk):
        data = self.get_object(pk)
        if not req.user.is_authenticated:
            raise NotAuthenticated
        if data.owner != req.user:
            raise PermissionDenied

        data.delete()
        return Response(status=HTTP_204_NO_CONTENT)


# from django.shortcuts import render
# from django.http import HttpResponse
# from .models import Room


# def see_all_rooms(req):
#     rooms = Room.objects.all()
#     return render(
#         req,
#         "all_rooms.html",
#         {"rooms": rooms, "title": "Hello This is django"},
#     )


# def see_one_rooms(req, room_pk):
#     try:
#         room = Room.objects.get(pk=room_pk)
#         return render(
#             req,
#             "room_detail.html",
#             {"room": room},
#         )
#     except Room.DoesNotExist:
#         return render(req, "room_detail.html", {"not_found": True})
