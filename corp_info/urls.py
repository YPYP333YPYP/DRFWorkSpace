from django.urls import path, include
from .views import update_corp_info, CorporationDetailAPIView, SmartLogisticsViewSet

urlpatterns = [
    path('corp_update/<str:name>', update_corp_info, name='update_corp_info'),
    path('corp_get/<str:corp_name>/', CorporationDetailAPIView.as_view(), name='corporation'),
    path('smarts/<str:port_name>/',SmartLogisticsViewSet.as_view({'get': 'list'}),name='smart-detail'),

]