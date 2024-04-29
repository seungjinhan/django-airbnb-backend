import jwt
import requests

from django.contrib.auth import authenticate, login, logout
from django.conf import settings

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


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, req):
        logout(req)
        return Response({"ok": "bye"})


class Login(APIView):
    def post(self, req):
        username = req.data.get("username")
        password = req.data.get("password")
        if not username or not password:
            raise exceptions.ParseError

        user = authenticate(req, username=username, password=password)
        if user:
            login(req, user)
            return Response({"ok": "welcome"})
        else:
            return Response({"error": "wrong password"})


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


class JWTLogin(APIView):
    def post(self, req):
        username = req.data.get("username")
        password = req.data.get("password")

        if not username or not password:
            raise exceptions.ParseError

        user = authenticate(
            req,
            username=username,
            password=password,
        )

        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response({"error": "wrong password"})


class GithugLogin(APIView):
    def post(self, req):
        try:
            code = req.data.get("code")
            access_token = requests.post(
                f"https://github.com/login/oauth/access_token?code={code}&client_id=123750bcf89f6b89694b&client_secret={settings.GITHUB_SECRET}",
                headers={"Accept": "application/json"},
            )
            access_token = access_token.json().get("access_token")

            user_data = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_data = user_data.json()

            user_email = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_email = user_email.json()
            email = user_email[0]["email"]
            try:
                user = User.objects.get(email=email)
                login(req, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("login"),
                    email=email,
                    name=user_data.get("name"),
                    avator=user_data.get("avatar_url"),
                )
                print(user)
                user.set_unusable_password()
                user.save()
                login(req, user)
                return Response(status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class KakaoLogin(APIView):
    def post(self, req):
        try:
            code = req.data.get("code")
            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
                },
                data={
                    "grant_type": "authorization_code",
                    "client_id": "5006367c6b8a3e5ab778b34c24a2e0cc",
                    "redirect_uri": "http://localhost:3001/social/kakao",
                    "code": code,
                },
            )
            access_token = access_token.json().get("access_token")

            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            user_data = user_data.json()
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")

            email = kakao_account.get("email")
            try:
                user = User.objects.get(email=email)
                login(req, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=profile.get("nickname"),
                    email=email,
                    name=profile.get("nickname"),
                    avator=profile.get("profile_image_url"),
                )
                user.set_unusable_password()
                user.save()
                login(req, user)
                return Response(status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
