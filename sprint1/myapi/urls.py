from django.urls import path
from .views import submitData

urlpatters = [
    path('submitData', submitData.as_view()),
]