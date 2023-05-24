from django.urls import path, include
from .views import update_corp_info, CorporationDetailAPIView

urlpatterns = [
    path('corp_update/<str:name>', update_corp_info, name='update_corp_info'),
    path('corp/<str:corp_name>/', CorporationDetailAPIView.as_view(), name='corporation')
]

