#!/usr/bin/env python
# coding: utf-8

# In[5]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime 
import sqlalchemy

# In[6]:


url = 'https://21cineplex.com/'
r = requests.get(url,verify=False)
soup = BeautifulSoup(r.content, 'html.parser')


# In[39]:
db = sqlalchemy.create_engine(
    # Equivalent URL:
    # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
    sqlalchemy.engine.url.URL(
        drivername="mysql+pymysql",
        username='robot',
        password='robot',
        database='cinema21_db',
        query={"unix_socket": "/cloudsql/{}".format(cloud_sql_connection_name)},
    ),
    # ... Specify additional properties here.
    # [START_EXCLUDE]
    # [START cloud_sql_mysql_sqlalchemy_limit]
    # Pool size is the maximum number of permanent connections to keep.
    pool_size=5,
    # Temporarily exceeds the set pool_size if no connections are available.
    max_overflow=2,
    # The total number of concurrent connections for your application will be
    # a total of pool_size and max_overflow.
    # [END cloud_sql_mysql_sqlalchemy_limit]
    # [START cloud_sql_mysql_sqlalchemy_backoff]
    # SQLAlchemy automatically uses delays between failed connection attempts,
    # but provides no arguments for configuration.
    # [END cloud_sql_mysql_sqlalchemy_backoff]
    # [START cloud_sql_mysql_sqlalchemy_timeout]
    # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
    # new connection from the pool. After the specified amount of time, an
    # exception will be thrown.
    pool_timeout=30,  # 30 seconds
    # [END cloud_sql_mysql_sqlalchemy_timeout]
    # [START cloud_sql_mysql_sqlalchemy_lifetime]
    # 'pool_recycle' is the maximum number of seconds a connection can persist.
    # Connections that live longer than the specified amount of time will be
    # reestablished
    pool_recycle=1800,  # 30 minutes
    # [END cloud_sql_mysql_sqlalchemy_lifetime]
    # [END_EXCLUDE]
)

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
	stmt = sqlalchemy.text(
        "INSERT INTO 21cineplex_trx  " " VALUES (:link, :name,:rating,:advance,:current_time)"
df = pd.DataFrame(data, columns = ['link','name','rating','is_advance','load_date'])
df.to_csv(str.replace(df.load_date.unique()[0],':','-')+'.csv')



