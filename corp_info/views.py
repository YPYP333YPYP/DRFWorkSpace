from django.shortcuts import render
from datetime import datetime, timedelta
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Corporation
import requests
import io
import zipfile
import xmltodict
import pandas as pd
import json


class Information:
    appkey = 'fb3196b97e3d77f755d9b061764117e1fa6e3596'

    def __init__(self):
        self.appkey = 'fb3196b97e3d77f755d9b061764117e1fa6e3596'

    def get_corp_code(self, name, appkey=None):
        if appkey is None:
            appkey = self.appkey

        url = "https://opendart.fss.or.kr/api/corpCode.xml"
        params = {
            "crtfc_key": appkey
        }
        response = requests.get(url, params=params)
        f = io.BytesIO(response.content)
        zfile = zipfile.ZipFile(f)
        zfile.namelist()
        xml = zfile.read("CORPCODE.xml").decode("utf-8")
        dict_data = xmltodict.parse(xml)
        data = dict_data['result']['list']
        df = pd.DataFrame(data)
        row = df[df['corp_name'] == name]

        return row['corp_code'].values[0]

    def get_corp_information(self, name, appkey=None):
        if appkey is None:
            appkey = self.appkey

        url = 'https://opendart.fss.or.kr/api/company.json'
        params = {
            "crtfc_key": appkey,
            "corp_code": self.get_corp_code(name, appkey)
        }
        response = requests.get(url, params=params)
        response = response.json()

        data = {'corp_name': response['corp_name'], 'ceo_name': response['ceo_nm'], 'corp_addr': response['adres'],
                'corp_homepage': response['hm_url'], 'phone_number': response['phn_no'], 'est_date': response['est_dt']}
        return data

    def get_corp_finance(self, name, appkey=None):
        if appkey is None:
            appkey = self.appkey

        now_year = '2022'
        url = 'https://opendart.fss.or.kr/api/fnlttSinglAcnt.json'
        params = {
            "crtfc_key": appkey,
            "corp_code": self.get_corp_code(name, appkey),
            "bsns_year": now_year,
            "reprt_code": '11011'
        }
        response = requests.get(url, params=params)
        response = response.json()
        response = response['list']

        fin_list = [value['thstrm_amount'] for value in response if
                    (value['account_nm'] == '매출액' or value['account_nm'] == '영업이익') and value['fs_div'] == 'CFS']
        sales_revenue = int(fin_list[0].replace(',', ''))
        operating_profit = int(fin_list[1].replace(',', ''))

        data = {'sales_revenue': f'{sales_revenue / 100000000:.1f} 억',
                'operating_profit': f'{operating_profit / 100000000:.1f} 억'}
        return data


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



