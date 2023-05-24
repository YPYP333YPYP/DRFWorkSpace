from django.shortcuts import render
from rest_framework import generics
from .serializers import CorporationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Corporation
from .information import Information


# 기업 정보를 직접 저장할 수 있는 GET API
@api_view(['GET'])
def update_corp_info(request, name):
    if request.method == 'GET':
        info = Information()
        corp_info = info.get_corp_information(name, info.appkey)
        corp_fin = info.get_corp_finance(name, info.appkey)
    try:
        corporation = Corporation.objects.get(corp_name=name)
        corporation.ceo_name = corp_info['ceo_name']
        corporation.corp_addr = corp_info['corp_addr']
        corporation.corp_homepage = corp_info['corp_homepage']
        corporation.phone_number = corp_info['phone_number']
        corporation.est_date = corp_info['est_date']
        corporation.sales_revenue = corp_fin['sales_revenue']
        corporation.operating_profit = corp_fin['operating_profit']
        corporation.save()  # Save the changes

        return Response({'message': '주식 정보가 업데이트되었습니다.'}, status=200)

    except Corporation.DoesNotExist:

        corporation = Corporation(
            corp_name=name,
            ceo_name=corp_info['ceo_name'],
            corp_addr=corp_info['corp_addr'],
            corp_homepage=corp_info['corp_homepage'],
            phone_number=corp_info['phone_number'],
            est_date=corp_info['est_date'],
            sales_revenue=corp_fin['sales_revenue'],
            operating_profit=corp_fin['operating_profit']
        )
        corporation.save()

        return Response({'message': '주식 정보가 업데이트되었습니다.'}, status=200)

# 기업 정보를 조회할 수 있는 GET API
class CorporationDetailAPIView(generics.RetrieveAPIView):
    queryset = Corporation.objects.all()
    serializer_class = CorporationSerializer
    lookup_field = 'corp_name'

