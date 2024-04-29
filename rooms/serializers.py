from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializer import TinyUserSerializer
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from wishlists.models import WishList


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomBaseSerializer(ModelSerializer):
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        req = self.context["req"]
        return room.owner == req.user

    class Meta:
        model = Room
        fields = ("rating", "is_owner", "photos")


class RoomDetailSerializer(RoomBaseSerializer):
    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta(RoomBaseSerializer.Meta):
        fields = "__all__"
        # fields = RoomBaseSerializer.Meta.fields
        # model = Room
        # fields = "__all__"
        # depth = 1

    def get_is_liked(self, room):
        req = self.context["req"]
        if req.user.is_authenticated:
            return WishList.objects.filter(
                user=req.user,
                rooms__id=room.pk,
            ).exists()
        return False

    # def get_rating(self, room):
    #     return room.rating()

    # def get_is_owner(self, room):
    #     req = self.context["req"]
    #     return room.owner == req.user


class RoomListSerializer(RoomBaseSerializer):

    # rating = serializers.SerializerMethodField()
    # is_owner = serializers.SerializerMethodField()

    class Meta(RoomBaseSerializer.Meta):
        # model = Room

        fields = RoomBaseSerializer.Meta.fields + (
            "pk",
            "name",
            "country",
            "city",
            "price",
        )

    # def get_rating(self, room):
    #     return room.rating()

    # def get_is_owner(self, room):
    #     req = self.context["req"]
    #     return room.owner == req.user
