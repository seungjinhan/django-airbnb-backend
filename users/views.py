from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializer import PrivateUserSerializer


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req):
        user = req.user
        return Response(PrivateUserSerializer(user).data)

    def put(self, req):
        user = req.user
        srz = PrivateUserSerializer(
            user,
            data=req.data,
            partial=True,
        )
        if srz.is_valid():
            user = srz.save()
            srz = PrivateUserSerializer(user)
            return Response(srz.data)
        else:
            return Response(srz.errors)
