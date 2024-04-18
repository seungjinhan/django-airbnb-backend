from django.shortcuts import render
from django.http import HttpResponse
from .models import Room


def see_all_rooms(req):
    rooms = Room.objects.all()
    return render(
        req,
        "all_rooms.html",
        {"rooms": rooms, "title": "Hello This is django"},
    )


def see_one_rooms(req, room_pk):
    try:
        room = Room.objects.get(pk=room_pk)
        return render(
            req,
            "room_detail.html",
            {"room": room},
        )
    except Room.DoesNotExist:
        return render(req, "room_detail.html", {"not_found": True})
