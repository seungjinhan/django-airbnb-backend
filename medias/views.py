from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from common import utils
from .models import Photo


class PhotoDetail(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, req, pk):
        photo = utils.get_object(Photo, pk)
        if (photo.room and photo.room.owner != req.user) or (
            photo.experience and photo.experience.host != req.user
        ):
            raise PermissionDenied

        photo.delete()

        return Response(status=HTTP_200_OK)


class GetUploadUrl(APIView):
    def post(self, req):
        pass
