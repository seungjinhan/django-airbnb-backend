from django.conf import settings
from django.db import transaction
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from common import utils
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer


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
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class AmenityDetail(APIView):
    # def get_object(self, pk):
    #     try:
    #         return Amenity.objects.get(pk=pk)
    #     except Amenity.DoesNotExist:
    #         raise NotFound

    def get(self, req, pk):
        amenity = utils.get_object(Amenity, pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, req, pk):
        amenity = utils.get_object(model=Amenity, pk=pk)
        serializer = AmenitySerializer(amenity, data=req.data, partial=True)
        if serializer.is_valid():
            update_amenity = serializer.save()
            return Response(AmenitySerializer(update_amenity).data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

    def delete(self, req, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, req):
        all_data = Room.objects.all()
        serializer = RoomListSerializer(
            all_data,
            many=True,
            context={"req": req},
        )
        return Response(serializer.data)

    def post(self, req):
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
                    room = serializer.save(owner=req.user, category=category)

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
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class RoomDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, req, pk):
        data = utils.get_object(Room, pk)
        serializer = RoomDetailSerializer(
            data,
            context={"req": req},
        )
        return Response(serializer.data)

    def put(self, req, pk):
        room = utils.get_object(model=Room, pk=pk)
        if room.owner != req.user:
            raise PermissionDenied

    def delete(self, req, pk):
        data = self.get_object(pk)
        if data.owner != req.user:
            raise PermissionDenied

        data.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, req, pk):
        # print(req.query_params)
        try:
            page = int(req.query_params.get("page", 1))
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        room = utils.get_object(Room, pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, req, pk):
        srz = ReviewSerializer(data=req.data)
        if srz.is_valid():
            review = srz.save(
                user=req.user,
                room=utils.get_object(Room, pk),
            )
            srz = ReviewSerializer(review)
            return Response(srz.data)


class RoomPhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, req, pk):
        room = utils.get_object(Room, pk)
        if req.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=req.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            return Response(PhotoSerializer(photo).data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class RoomBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, req, pk):
        room = utils.get_object(model=Room, pk=pk)
        now = timezone.localtime(timezone.now()).date()

        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gt=now,
        )
        srz = PublicBookingSerializer(
            bookings,
            many=True,
        )
        return Response(srz.data)

    def post(self, req, pk):
        room = utils.get_object(
            model=Room,
            pk=pk,
        )
        srz = CreateRoomBookingSerializer(data=req.data)
        if srz.is_valid():
            booking = srz.save(
                room=room,
                user=req.user,
                kind=Booking.BookingKindChoices.ROOM,
            )
            srz = PublicBookingSerializer(booking)
            return Response(srz.data)
        else:
            return Response(
                srz.errors,
                status=HTTP_400_BAD_REQUEST,
            )


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
