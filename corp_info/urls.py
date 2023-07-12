from django.urls import path, include
from .views import update_corp_info, CorporationDetailAPIView, SmartLogisticsViewSet, RecruitmentAPIView, RecruitmentListAPIView

urlpatterns = [
    path('update_corp/<str:name>', update_corp_info, name='update_corp_info'),
    path('get_corp/<str:corp_name>/', CorporationDetailAPIView.as_view(), name='corporation'),
    path('get_smart_tech/<str:port_name>/', SmartLogisticsViewSet.as_view({'get': 'list'}), name='smart-detail'),
    path('save_recruit/<str:code>/', RecruitmentAPIView.as_view(), name='update_recruitment'),
    path('get_recruit/<str:code>/', RecruitmentListAPIView.as_view(), name='get_recruitment')
]