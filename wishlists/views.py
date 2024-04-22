from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rooms.models import Room
from .models import WishList
from .serializers import WishListSerializer
from common import utils


class WishListView(APIView):
    def get(self, req):
        all_wishlists = WishList.objects.filter(user=req.user)
        srz = WishListSerializer(
            all_wishlists,
            many=True,
            context={"req": req},
        )
        return Response(srz.data)

    def post(self, req):
        srz = WishListSerializer(data=req.data)
        if srz.is_valid():
            data = srz.save(user=req.user)
            srz = WishListSerializer(data)
            return Response(srz.data)
        else:
            return Response(srz.errors)


class WishListDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, req, pk):
        data = utils.get_object(model=WishList, pk=pk, user=req.user)
        srz = WishListSerializer(data, context={"req": req})
        return Response(srz.data)

    def delete(self, req, pk):
        data = utils.get_object(model=WishList, pk=pk, user=req.user)
        data.delete()
        return Response(status=HTTP_200_OK)

    def put(self, req, pk):
        data = utils.get_object(model=WishList, pk=pk, user=req.user)
        srz = WishListSerializer(data, data=req.data, partial=True)
        if srz.is_valid():
            data = srz.save()
            srz = WishListSerializer(data)
            return Response(srz.data)
        else:
            return Response(srz.errors)


class WishListToggle(APIView):

    def put(self, req, pk, room_pk):
        wishlist = utils.get_object(model=WishList, pk=pk, user=req.user)
        room = utils.get_object(model=Room, pk=room_pk)

        if wishlist.rooms.filter(pk=room.pk).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)

        return Response(status=HTTP_200_OK)
