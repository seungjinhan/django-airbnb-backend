import jwt

from django.conf import settings

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from users.models import User
from common import utils


class TrustMeBroAuthentication(BaseAuthentication):
    def authenticate(self, req):
        username = req.headers.get("trust-me")
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed(f"No User {username}")


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.headers.get("jwt")
        if not token:
            return None

        decoded = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms="HS256",
        )
        pk = decoded.get("pk")
        if not pk:
            raise AuthenticationFailed("Invalid Token")

        user = utils.get_object(
            model=User,
            pk=pk,
            not_found_exception=AuthenticationFailed("User Not Found"),
        )

        return (user, None)
