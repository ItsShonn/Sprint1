from django.core.exceptions import ValidationError

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
            try:
                coords = Coords(latitude=float(d.get('coords')['latitude']),
                                               longitude=float(d.get('coords')['longitude']),
                                               height=int(d.get('coords')['height']))
                coords.save()
                objects_.append(coords)
                if not (User.objects.filter(pk=d.get('user').get('email')).exists()):
                    return Response({"status":500, "message":"Неизвестный пользователь", "id":0})

                pereval_added = PerevalAdded(beautyTitle=d.get('beauty_title'),
                                             title=d.get('title'),
                                             otherTitles=d.get('other_titles'),
                                             connect=d.get('connect'),
                                             add_time=d.get('add_time'),
                                             user=User.objects.get(pk=d.get('user')['email']),
                                             spring=d.get('level')['spring'],
                                             summer=d.get('level')['summer'],
                                             autumn=d.get('level')['autumn'],
                                             winter=d.get('level')['winter'],
                                             coords_id=coords)
                pereval_added.save()
                objects_.append(pereval_added)

                for image in d.get('images'):
                    img = Images(img=str.encode(image.get('data')),
                                 title=image.get('title'))
                    img.save()
                    objects_.append(img)

                    per_img = PerevalImages(pereval_id=pereval_added,
                                            image_id=img)
                    per_img.save()
                    objects_.append(per_img)
            except ValidationError as e:
                for obj in objects_:
                    obj.delete()
                return Response({"status":400, "message":f"Невалидные данные: {e}", "id":0})
            return Response({"status":200, "message":0, "id":pereval_added.id})
        return Response({"status":400, "message":"Невалидный запрос", "id":0})