from django.urls import path
from .views import Me, Users, PublicUser, ChangePassword, Login, Logout

urlpatterns = [
    path("", Users.as_view()),
    path("me", Me.as_view()),
    path("change-password", ChangePassword.as_view()),
    path("log-in", Login.as_view()),
    path("log-out", Logout.as_view()),
    path("@<str:username>", PublicUser.as_view()),
]
