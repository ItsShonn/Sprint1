from .models import *
from rest_framework import serializers
import json


class PerevalSerializer(serializers.Serializer):
   beauty_title = serializers.CharField()
   title = serializers.CharField()
   other_titles = serializers.CharField()
   connect = serializers.CharField(allow_blank=True)
   add_time = serializers.DateTimeField()
   user = serializers.JSONField()
   coords = serializers.JSONField()
   level = serializers.JSONField()
   images = serializers.ListField()

   def validate(self, data):
       d_user = data['user']
       d_coords = data['coords']
       d_level = data['level']
       d_images = data['images']

       if set(d_user.keys()) != {'email', 'fam', 'name', 'otc', 'phone'}:
               raise serializers.ValidationError(f'Not enough fields')

       if set(d_coords.keys()) != {'longitude', 'latitude', 'height'}:
               raise serializers.ValidationError('Not enough fields')

       if set(d_level.keys()) != {'spring', 'winter', 'autumn', 'summer'}:
               raise serializers.ValidationError('Not enough fields')

       for f in d_images:
           if tuple(f.keys()) != ('data', 'title'):
               raise serializers.ValidationError('Not enough fields')

       return data
