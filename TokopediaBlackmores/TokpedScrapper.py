import json
import urllib.request
from pandas.io.json import json_normalize
import requests
import pandas as pd
import csv
import re
import time
from datetime import date
import os
from bs4 import BeautifulSoup
import sqlite3

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
def search(keyword):
    #mengambil jumlah data keseluruhan dari tokopedia sesuai keyword
    url1  = ("https://ace.tokopedia.com/search/product/v3?scheme=https&device=desktop&related=true&catalog_rows=5&source=recent&ob=23&st=product&rows=1&start=0&q={}&unique_id=f198715c44b1415e8872f60e367aaa4b&safe_search=false").format(keyword)
    headers = {"User-Agent":UA}
    data = requests.get(url1, headers=headers).content.decode("utf-8")
    total_data = re.findall(r'(?:"total_data_text":")(.*?)(?:")', data)
    total_data_clean = [x.replace(".", "") for x in total_data]
    total_data_int = list(map(int, total_data_clean))[0]
    result = []
    for baris in range (0, total_data_int, 60):
        url = ("https://ace.tokopedia.com/search/product/v3?scheme=https&device=desktop&related=true&catalog_rows=5&source=recent&ob=23&st=product&rows=60&q={}&start={}&unique_id=f198715c44b1415e8872f60e367aaa4b&safe_search=false").format(keyword, baris)
        headers = {"User-Agent":UA}
        time.sleep(1)
        data_ = requests.get(url, headers=headers).content.decode("utf-8")
        data_ = json.loads(data_)['data']['products']
        data_frame = pd.io.json.json_normalize(data_)
        result.append(data_frame)
        MasterDF = pd.concat(result)
        data_final = MasterDF[['bottom_label','category_breadcrumb','category_id','category_name','childs','condition','count_review','courier_count','department_id','department_name','discount_expired','discount_percentage','discount_start','free_ongkir.img_url','free_ongkir.is_active','id','is_featured','is_preorder','min_order','name','original_price','parent_id','price','price_int','price_range','rating','shop.city','shop.id','shop.is_gold','shop.is_official','shop.is_power_badge','shop.location','shop.name','shop.reputation','shop.url','sku','status','stock','top_label','url','warehouse_id_default']]   
        data_final['get_date'] = date.today()
        data_final['keyword'] = keyword
    return data_final
#     MasterDF.to_csv(keyword+".csv")

if __name__ == "__main_":
    data_produk = pd.read_csv('D:\Project\phiradata\TokopediaBlackmores\Data Blackmores Kalbestore.csv')
    a = data_produk['nama_produk'][0]
    my_new_string = re.sub('[^a-zA-Z0-9 \n\.]', '', a)
    # my_new_string
    i = 1
    for prd in data_produk['nama_produk']:
        data_crawling = search(prd)
        data_crawling.to_csv(re.sub('D:\Project\phiradata\TokopediaBlackmores\1'+'[^a-zA-Z0-9 \n\.]', '', prd)+'.csv')
        print(str(i) + ' - '+ prd)
        i=i+1