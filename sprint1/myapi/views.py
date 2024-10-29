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
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)