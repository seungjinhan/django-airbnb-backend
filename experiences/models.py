from django.db import models
from common.models import CommonModel


class Experience(CommonModel):
    """Experience Definition"""

    name = models.CharField(max_length=250, default="")
    country = models.CharField(max_length=50, default="SouthKorea")
    city = models.CharField(max_length=80, default="Seoul")
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250)
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    perks = models.ManyToManyField(
        "experiences.Perk",
        related_name="experiences",
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="experiences",
    )

    def __str__(self) -> str:
        return self.name


class Perk(CommonModel):
    """what is included on an Experience"""

    name = models.CharField(max_length=100)
    details = models.CharField(max_length=250, blank=True, default="")
    explanation = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return self.name
