from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated

from .serializer import PrivateUserSerializer
from .models import User


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


class PublicUser(APIView):
    def get(self, req, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.NotFound

        srz = PrivateUserSerializer(user)
        return Response(srz.data)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, req):
        user = req.user
        old_pw = req.data.get("old_password")
        new_pw = req.data.get("new_password")
        if not old_pw or not new_pw:
            raise exceptions.ParseError

        if user.check_password(old_pw):
            user.set_password(new_pw)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Users(APIView):

    def post(self, req):
        password = req.data.get("password")
        if not password:
            raise exceptions.ParseError

        srz = PrivateUserSerializer(data=req.data)
        if srz.is_valid():
            user = srz.save()
            user.set_password(password)
            user.save()
            srz = PrivateUserSerializer(user)
            return Response(srz.data)
        else:
            return Response(srz.errors)
