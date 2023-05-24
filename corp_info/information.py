import requests
import io
import zipfile
import xmltodict
import pandas as pd
from datetime import datetime


# 기업 정보 Class (기업 정보, 재무 정보)
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

        if row.empty:
            raise ValueError("일치하는 회사 이름이 없습니다.")

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
        now_date = datetime.now()
        now_year = now_date.year
        if now_date >= datetime(now_year, 4,1):
            now_year = now_year - 1
        else:
            now_year = now_year - 2

        url = 'https://opendart.fss.or.kr/api/fnlttSinglAcnt.json'
        params = {
            "crtfc_key": appkey,
            "corp_code": self.get_corp_code(name, appkey),
            "bsns_year": now_year,
            "reprt_code": '11011'
        }
        response = requests.get(url, params=params)
        response = response.json()
        if response['status'] == '000':
            response = response['list']

            fin_list = [value['thstrm_amount'] for value in response if
                        (value['account_nm'] == '매출액' or value['account_nm'] == '영업이익') and value['fs_div'] == 'CFS']
            sales_revenue = int(fin_list[0].replace(',', ''))
            operating_profit = int(fin_list[1].replace(',', ''))

            data = {'sales_revenue': f'{sales_revenue / 100000000:.1f} 억',
                    'operating_profit': f'{operating_profit / 100000000:.1f} 억'}
            return data
        else:
            raise ValueError("일치하는 사업보고서가 없습니다.")