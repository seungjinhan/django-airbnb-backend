from common import utils

from . import models


def get_all_rooms():
    return models.Room.objects.all()


def get_room(pk: int):
    return utils.get_object(model=models.Room, pk=pk)
