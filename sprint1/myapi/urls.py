from django.urls import path, include
from .views import submitDataPOST, submitDataGET, submitDataEMAILGET
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('submitData', submitDataPOST.as_view()),
    path('submitData/<int:pk>', submitDataGET.as_view()),
    path('submitData/', submitDataEMAILGET.as_view()),
    path(
        "openapi",
        get_schema_view(
            title="FSTRAPI", description="API for FSTR app", version="1.0.0", urlconf='myapi.urls'
        ),
        name="openapi-schema"),
]