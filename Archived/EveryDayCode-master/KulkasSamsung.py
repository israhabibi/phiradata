from bs4 import BeautifulSoup
import pandas as pd
import glob
import requests
from selenium import webdriver

url = 'https://www.samsung.com/id/refrigerators/all-refrigerators/'
# r = requests.get(url)
# soup = BeautifulSoup(r.content, 'html.parser')
driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url)

html_source = driver.page_source
soup = BeautifulSoup(html_source, 'html.parser')

dataSamsung = []
shopGridd = soup.find('div', class_ = 'shop-grid')
listKulkases = shopGridd.find_all('div', class_ = 'shop-grid-col shop-col3')
for listKulkas in listKulkases:
    tipeKulkas = listKulkas.find('span', class_ = 'cm-shop-card__serial').get_text()
    namaKulkas = listKulkas.find('strong', class_ = 's-txt-title').get_text()
    try :
        hargaKulkas = listKulkas.find('span', class_ = 'cm-shop-card__price-num').get_text()
    except :
        hargaKulkas = 0
    dataSamsung.append((tipeKulkas,namaKulkas,hargaKulkas))

df = pd.DataFrame(dataSamsung,columns=['tipeKulkas','namaKulkas','hargaKulkas'])

df.to_csv('D:\\Project\\EveryDayCode\\TokPedScrapperOut\\'+'KulkasSamsung.csv')