from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import Perk
from .serializers import PerkSerializer


class Perks(APIView):
    def get(self, req):
        all_data = Perk.objects.all()
        serializer = PerkSerializer(all_data, many=True)
        return Response(serializer.data)

    def post(self, req):
        serializer = PerkSerializer(data=req.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response(PerkSerializer(data).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects().get(pk=pk)
        except:
            raise NotFound

    def get(self, req, pk):
        data = self.get_object(pk)
        serializer = PerkSerializer(data)
        return Response(serializer.data)

    def put(self, req, pk):
        data = self.get_object(pk)
        serializer = PerkSerializer(data, data=req.data, partial=True)
        if serializer.is_valid():
            update_data = serializer.save()
            return Response(PerkSerializer(update_data).data)
        else:
            return Response(serializer.errors)

    def delete(self, req, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)
