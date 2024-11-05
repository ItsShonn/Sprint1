from django.core.exceptions import ValidationError

from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
import json

from .serializers import *
from .models import *


class submitDataPOST(views.APIView):

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


class submitDataGET(views.APIView):

    def get(self, request, format=None, **kwargs):
        try:
            pk = kwargs.get('pk')
            pereval = PerevalAdded.objects.filter(pk=pk)
            if not(pereval.exists()) == True:
                return Response({"status":400, "message":"Объекта нет в базе данных", "id":0})
            pereval = pereval.first()
            coords = pereval.coords_id

            return Response({
                "status":200,
                "object":{"id": f"{pereval.id}",
                 "time_added": f"{pereval.time_added}",
                 "beautyTitle": f"{pereval.beautyTitle}",
                 "otherTitles": f"{pereval.otherTitles}",
                 "connect": f"{pereval.connect}",
                 "add_time": f"{pereval.add_time}",
                 "spring": f"{pereval.spring}",
                 "summer": f"{pereval.summer}",
                 "autumn": f"{pereval.autumn}",
                 "winter": f"{pereval.winter}",
                 "latitude": f"{coords.latitude}",
                 "longitude": f"{coords.longitude}",
                 "height": f"{coords.height}",
                 "user": f"{pereval.user.email}", }
            })
        except Exception as e:
            return Response({"status":500, "message":f"Ошибка {e}", "id":0})

    def patch(self, request, format=None, **kwargs):
        try:
            objects_ = []
            pk = kwargs.get('pk')
            pereval = PerevalAdded.objects.filter(pk=pk)
            if not(pereval.exists()) == True:
                return Response({"state":0, "message":"Объекта нет в базе данных"})
            pereval = pereval.first()

            if pereval.status == 'n':

                data = request.data
                serializer = PerevalSerializer(data=data)

                if not serializer.is_valid():
                    return Response({"state":0, "message":"Невалидный запрос"})
                d = serializer.data

                coords = pereval.coords_id
                coords.latitude = float(d['coords']['latitude'])
                coords.longitude = float(d['coords']['longitude'])
                coords.height = int(d['coords']['height'])

                level = d['level']
                pereval.spring = level['spring']
                pereval.summer = level['summer']
                pereval.autumn = level['autumn']
                pereval.winter = level['winter']

                old_per_imgs = PerevalImages.objects.filter(pereval_id=pereval)
                old_imgs = []
                for old_per_img in old_per_imgs:
                    old_imgs.append(old_per_img.image_id)

                for image in d.get('images'):
                    img = Images(img=str.encode(image.get('data')),
                                 title=image.get('title'))
                    img.save()
                    objects_.append(img)

                    per_img = PerevalImages(pereval_id=pereval,
                                            image_id=img)
                    per_img.save()
                    objects_.append(per_img)

                pereval.beautyTitle = d['beauty_title']
                pereval.title = d['title']
                pereval.otherTitles = d['other_titles']
                pereval.connect = d['connect']
                pereval.add_time = d['add_time']
                return pereval, coords, old_per_imgs, old_imgs
            else:
                return Response({"state":0, "message": "Запись не новая"})

        except Exception as e:
            for obj in objects_:
                obj.delete()
            return Response({"state": 0, "message": f"Ошибка {e}"})
        finally:
            try:
                pereval.save()
                coords.save()
                for per_img in old_per_imgs:
                    per_img.delete()
                for old_img in old_imgs:
                    old_img.delete()

                return Response({"state": 1, "message":None})
            except Exception:
                for obj in objects_:
                    obj.delete()


class submitDataEMAILGET(views.APIView):

    def get(self, request, format=None):
        email = request.query_params.get('user_email')
        user = User.objects.filter(email=email)
        if not user.exists():
            return Response({"state":0, "message":"Пользователя с такой почтой не существует", "result":None})
        perevals = PerevalAdded.objects.filter(user=user.first())
        res = []

        for pereval in perevals:
            coords = pereval.coords_id

            res.append({
                "status": 200,
                "object": {"id": f"{pereval.id}",
                           "time_added": f"{pereval.time_added}",
                           "beautyTitle": f"{pereval.beautyTitle}",
                           "otherTitles": f"{pereval.otherTitles}",
                           "connect": f"{pereval.connect}",
                           "add_time": f"{pereval.add_time}",
                           "spring": f"{pereval.spring}",
                           "summer": f"{pereval.summer}",
                           "autumn": f"{pereval.autumn}",
                           "winter": f"{pereval.winter}",
                           "latitude": f"{coords.latitude}",
                           "longitude": f"{coords.longitude}",
                           "height": f"{coords.height}",
                           "user": f"{pereval.user.email}", }
            })

        return Response({"state":1, "message":None, "result": res})