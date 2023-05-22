from django.shortcuts import render

# todo
"""
    < 기업 공시 >
    1. 종목 코드 입력시 공시 데이터를 DB에 저장하는 Get API 생성
    2. django-crontab을 이용하여 django 스케줄러에서 일주일마다 호출
    3. client 입장에서 종목 코드 ID 를 이용하여 JSON 객체로 DB의 기업 정보를 넘기는 Get API 생성
"""

#from datetime import datetime, timedelta
# import requests
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Stock
#
#
# @api_view(['GET'])
# def update_stock_info(request):
#     # Dart Open API에서 주식 종목 정보 가져오기
#     api_key = 'YOUR_DART_OPEN_API_KEY'
#     url = f'https://api.dart.or.kr/v1/company/fs_annual.json?auth={api_key}&crp_cd={stock_code}'
#
#     try:
#         response = requests.get(url)
#         data = response.json()
#         stock_info = data['stock_info']
#
#         # 데이터베이스에 주식 정보 저장하기
#         for stock_data in stock_info:
#             stock_code = stock_data['stock_code']
#             stock_name = stock_data['stock_name']
#             # ... 여기에 필요한 주식 정보를 추출하여 저장하는 로직을 작성하세요 ...
#             # 예를 들어, Stock 모델을 사용한다고 가정하면:
#             Stock.objects.update_or_create(
#                 stock_code=stock_code,
#                 defaults={
#                     'stock_name': stock_name,
#                     # ... 필요한 다른 필드들을 여기에 추가하세요 ...
#                 }
#             )
#
#         return Response({'message': '주식 정보가 업데이트되었습니다.'}, status=200)
#
#     except requests.exceptions.RequestException as e:
#         return Response({'message': f'API 요청에 실패했습니다: {str(e)}'}, status=500)

