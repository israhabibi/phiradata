# import lib
from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime

url = 'https://21cineplex.com/'
r = requests.get(url,verify=False)
soup = BeautifulSoup(r.content, 'html.parser')

data = []
now_playing= soup.find('div', id = 'now-playing')
list_movies = now_playing.find_all('div', class_ = 'col-3')
current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
for movie in list_movies :
    link = movie.find('a').get('href')
    name = movie.find('h4').get_text()
    rating = movie.find('span', class_ = 'movie-label').find('img').get('alt')
    try :
        advance = movie.find('span', class_ = 'movie-advanced').get_text()
    except :
        advance = ''
    data.append((link,name,rating,advance,current_time))
df = pd.DataFrame(data, columns = ['link','name','rating','is_advance','load_date'])
df.to_csv('data/'+str.replace(df.load_date.unique()[0],':','-')+'.csv')
