import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://dantri.com.vn/xa-hoi.htm"
 response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    main_div = soup.find('div', class_='main')
    article_list = main_div.find('div', class_='article list')
    articles = article_list.find_all('article', class_='article-item')