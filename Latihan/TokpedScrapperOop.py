import requests
import re
import json
import time
import pandas as pd
from datetime import date

class tokpedScrap:
    
    def __init__(self, keyword):
        self.keyword = keyword
        self.UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"

    def getTotalData(self):
        UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
        url  = ("https://ace.tokopedia.com/search/product/v3?scheme=https&device=desktop&related=true&catalog_rows=5&source=recent&ob=23&st=product&rows=1&start=0&q={}&unique_id=f198715c44b1415e8872f60e367aaa4b&safe_search=false").format(self.keyword)
        headers = {"User-Agent":UA}
        data = requests.get(url, headers=headers).content.decode("utf-8")
        jsonData = json.loads(data)
        totalData = jsonData['header']['total_data']
        return totalData

    def getProductData(self, totalData):
        result = []
        for baris in range (0, totalData, 60):
            url = ("https://ace.tokopedia.com/search/product/v3?scheme=https&device=desktop&related=true&catalog_rows=5&source=recent&ob=23&st=product&rows=60&q={}&start={}&unique_id=f198715c44b1415e8872f60e367aaa4b&safe_search=false").format(self.keyword, baris)
            headers = {"User-Agent":self.UA}
            time.sleep(1)
            dataJson = requests.get(url, headers=headers).content.decode("utf-8")
            dataJson = json.loads(dataJson)['data']['products']
            dataFrame = pd.json_normalize(dataJson)
            result.append(dataFrame)
            masterDF = pd.concat(result)
            dataFinal = masterDF[['bottom_label','category_breadcrumb','category_id','category_name','childs','condition','count_review','courier_count','department_id','department_name','discount_expired','discount_percentage','discount_start','free_ongkir.img_url','free_ongkir.is_active','id','is_featured','is_preorder','min_order','name','original_price','parent_id','price','price_int','price_range','rating','shop.city','shop.id','shop.is_gold','shop.is_official','shop.is_power_badge','shop.location','shop.name','shop.reputation','shop.url','sku','status','stock','top_label','url','warehouse_id_default']]   
            dataFinal['get_date'] = date.today()
            dataFinal['keyword'] = self.keyword
        return dataFinal

    def toCsv (self, dataFinal):
        dataFinal.to_csv(self.keyword+str(date.today())+'.csv')
        
if __name__ == "__main__":
    tokpedScrap = tokpedScrap('KulKas Samsung')
    tData = tokpedScrap.getTotalData()
    print(tData)
    dFinal = tokpedScrap.getProductData(tData)
    tokpedScrap.toCsv(dFinal)