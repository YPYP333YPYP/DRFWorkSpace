from django.urls import path
from .views import update_corp_info

urlpatterns = [
    path('corp_update/<str:name>', update_corp_info, name='update_corp_info'),
]
