import typing
from django.conf import settings

import strawberry
from strawberry import auto
from strawberry.types import Info

from . import models
from users.types import UserType
from reviews.types import ReviewType
from wishlists.models import WishList


@strawberry.django.type(models.Room)
class RoomType:
    id: auto
    name: auto
    kind: auto
    owner: "UserType"

    @strawberry.field
    def reviews(self, page: int) -> typing.List["ReviewType"]:
        page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        return self.reviews.all()[start:end]

    @strawberry.field
    def rating(self) -> str:
        return self.rating()

    @strawberry.field
    def is_owner(self, info: Info) -> bool:
        return self.owner == info.context.request.user

    @strawberry.field
    def is_liked(self, info: Info) -> bool:
        return WishList.objects.filter(
            user=info.context.request.user,
            rooms__pk=self.pk,
        ).exists()
