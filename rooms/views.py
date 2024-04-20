from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Amenity
from .serializers import AmenitySerializer


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
