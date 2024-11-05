from django.urls import path, include
from .views import submitDataPOST, submitDataGET, submitDataEMAILGET

urlpatterns = [
    path('submitData', submitDataPOST.as_view()),
    path('submitData/<int:pk>', submitDataGET.as_view()),
    path('submitData/', submitDataEMAILGET.as_view()),
]