from .models import *
from rest_framework import serializers
import json


class PerevalSerializer(serializers.Serializer):
   beautyTitle = serializers.CharField()
   title = serializers.CharField()
   other_titles = serializers.CharField()
   connect = serializers.CharField()
   add_time = serializers.DateTimeField()
   user = serializers.JSONField()
   coords = serializers.JSONField()
   level = serializers.JSONField()
   images = serializers.ListField()

   def validate(self, data):

       d_user = data['user']
       d_user = json.loads(d_user)
       d_coords = data['coords']
       d_coords = json.loads(d_coords)
       d_level = data['level']
       d_level = json.loads(d_level)
       d_images = data['images']

       for f in d_user.values():
           if not(f in ['email', 'fam', 'name', 'otc', 'phone']):
               raise serializers.ValidationError('Not enough fields')

       for f in d_coords.values():
           if not(f in ['longitude', 'latitude', 'height']):
               raise serializers.ValidationError('Not enough fields')

       for f in d_level.values():
           if not(f in ['spring', 'winter', 'autumn', 'summer']):
               raise serializers.ValidationError('Not enough fields')

       for f in d_images:
           if tuple(f.keys()) != ('data', 'title'):
               raise serializers.ValidationError('Not enough fields')

       return data
