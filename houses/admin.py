from django.contrib import admin
from .models import House


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):

    fields = ("name", 'address', ("price_per_night", "pet_allowed"), "owner")
    list_display = (
        "name", "price_per_night", "address", 'pet_allowed'
    )

    list_filter = ('price_per_night', 'pet_allowed', )

    search_fields = ('address__startswith', )

    list_display_links = ('name', 'address')

    list_editable = ("pet_allowed", 'price_per_night')
