from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import Me, Users, PublicUser, ChangePassword, Login, Logout

urlpatterns = [
    path("", Users.as_view()),
    path("me", Me.as_view()),
    path("change-password", ChangePassword.as_view()),
    path("log-in", Login.as_view()),
    path("log-out", Logout.as_view()),
    path("token-login", obtain_auth_token),
    path("@<str:username>", PublicUser.as_view()),
]
