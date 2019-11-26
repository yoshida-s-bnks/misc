import urllib.request, urllib.error
from bs4 import BeautifulSoup
import datetime
import csv
import os

url = "http://www.nikkei.com"

html = urllib.request.urlopen(url)

f = open(os.environ['DATA_PATH']+'/mkt/mkt-data-dump.csv','a')
writer = csv.writer(f)

soup = BeautifulSoup(html, "html.parser")
uls = soup.find_all('ul', class_='k-hub-market__content')

now = datetime.datetime.now().year

for ul_tag in uls:
    for li_tag in ul_tag.find_all('li', class_='k-hub-market__index'):
        csv_list = []
        csv_list.append(li_tag.find('span').previousSibling)
        t_stamp = str(now) +'/'+ li_tag.find('a').get('title').strip(' ''大引’’終値').replace('月','/').replace('日','')
        csv_list.append(t_stamp)
        csv_list.append(li_tag.find('span', class_='k-hub-market__current-price').text.replace(',',''))

        print(csv_list)
        writer.writerow(csv_list)

f.close
