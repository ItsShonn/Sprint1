from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
import json

from .serializers import *
from .models import *


class submitData(views.APIView):

    def post(self, request, format=None):
        data = request.data
        serializer = PerevalSerializer(data=data)

        if serializer.is_valid():
            d = serializer.data
            objects_ = []

            coords = Coords(latitude=float(d.get('coords')['latitude']),
                                           longitude=float(d.get('coords')['longitude']),
                                           height=int(d.get('coords')['height']))
            coords.save(commit=False)
            objects_.append(coords)
            if not (User.objects.filter(d.get('user')['email']).exists()):
                return Response({"status":500, "message":"Неизвестный пользователь", "id":0})

            pereval_added = PerevalAdded(beautyTitle=d.get('beauty_title'),
                                         title=d.get('title'),
                                         otherTitles=d.get('other_titles'),
                                         connect=d.get('connect'),
                                         add_time=d.get('add_time'),
                                         user=d.get('user')['email'],
                                         spring=d.get('level')['spring'],
                                         summer=d.get('level')['summer'],
                                         autumn=d.get('level')['autumn'],
                                         winter=d.get('level')['winter'],
                                         coords_id=coords.id)
            pereval_added.save(commit=False)
            objects_.append(pereval_added)
            for image in d.get('images'):
                img = Images(img=image.get('data'),
                             title=image.get('title'))
                img.save(commit=False)
                per_img = PerevalImages(pereval_id=pereval_added.id,
                                        image_id=img.id)
                objects_.append(img)
                objects_.append(per_img)

            if all([obj.is_valid() for obj in objects_]):
                for obj in objects_:
                    obj.save()

            return Response({"status":200, "message":0, "id":pereval_added.id})
        return Response({"status":400, "message":"Невалидный запрос", "id":0})