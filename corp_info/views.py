from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CorporationSerializer, SmartLogisticsSerializer, RecruitmentSerializer
from .models import Corporation, SmartLogistics, Recruitment
from .information import Information
from .recruitment import get_recruit, save_recruitment_data


# 기업 정보를 직접 저장할 수 있는 GET API
@api_view(['GET'])
def update_corp_info(request, name):
    if request.method == 'GET':
        info = Information()
        try:
            corp_info = info.get_corp_information(name, info.appkey)
            corp_fin = info.get_corp_finance(name, info.appkey)
        except ValueError:
            raise NotFound("정상적이지 않은 값이 입력되었습니다.")
    try:
        corporation = Corporation.objects.get(corp_name=name)
        corporation.ceo_name = corp_info['ceo_name']
        corporation.corp_addr = corp_info['corp_addr']
        corporation.corp_homepage = corp_info['corp_homepage']
        corporation.phone_number = corp_info['phone_number']
        corporation.est_date = corp_info['est_date']
        corporation.sales_revenue = corp_fin['sales_revenue']
        corporation.operating_profit = corp_fin['operating_profit']
        corporation.save()

        return Response({'message': '기업 정보가 업데이트되었습니다.'}, status=200)

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

        return Response({'message': '기업 정보가 업데이트되었습니다.'}, status=200)


# 기업 정보를 조회할 수 있는 GET API
class CorporationDetailAPIView(generics.RetrieveAPIView):
    queryset = Corporation.objects.all()
    serializer_class = CorporationSerializer
    lookup_field = 'corp_name'

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        corp_name = self.kwargs['corp_name']
        try:
            obj = queryset.get(corp_name=corp_name)
            return obj
        except Corporation.DoesNotExist:
            raise NotFound('일치하는 기업이 없습니다.')

# 스마트해상물류 기술을 조회할 수 있는 GET API
class SmartLogisticsViewSet(viewsets.ModelViewSet):
    serializer_class = SmartLogisticsSerializer
    queryset = SmartLogistics.objects.all()
    lookup_field = 'port_name'

    def get_queryset(self):
        port_name = self.kwargs['port_name']
        queryset = SmartLogistics.objects.filter(port_name=port_name)
        return queryset

    @action(detail=False, methods=['get'], url_path='<str:port_name>/')
    def get_by_port_name(self, request, port_name=None):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, port_name=port_name)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# 직업코드 별 채용정보를 저장할 수 있는 GET API
class RecruitmentAPIView(APIView):
    def get(self, request, code):
        data = get_recruit(code)

        if data:
            save_recruitment_data(data)
            return Response({'message': code + '채용정보에 대한 채용정보가 업데이트 되었습니다.'})
        else:
            raise NotFound('채용정보가 정상적으로 업데이트 되지 않았습니다')


class RecruitmentListAPIView(APIView):
    def get(self, request, code):
        recruitments = Recruitment.objects.filter(code=code)
        serializer = RecruitmentSerializer(recruitments, many=True)
        return Response(serializer.data)