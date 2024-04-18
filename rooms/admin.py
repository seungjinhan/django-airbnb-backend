from django.contrib import admin
from .models import Room, Amenity


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "total_amenities",
        "rating",
        "kind",
        "owner",
        "created_at",
    )
    list_filter = (
        "country",
        "city",
        "pet_friendly",
        "kind",
        "amenities",
        "created_at",
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_filter = ("name", "description", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
