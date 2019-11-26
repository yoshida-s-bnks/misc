import urllib.request, urllib.error
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os

url = "http://gold.tanaka.co.jp/index.php"

html = urllib.request.urlopen(url)

#f = open('~/data/mkt/mkt-data-storage.csv','a')
f = open(os.environ['DATA_PATH']+'/mkt/mkt-data-dump.csv','a')
writer = csv.writer(f)

soup = BeautifulSoup(html, "html.parser")
div_ = soup.find('div', id='soba_info')
t_stamp = div_.find('p', id='release_time').text.strip('公表')

for li_tag in div_.find_all('li'):
    csv_list = []
    csv_list.append(li_tag.find('span').previousSibling)
    csv_list.append(t_stamp)
    csv_list.append(li_tag.find('br').previousSibling.strip('円').replace(',',''))
#        csv_list.append(span_tag.text)

    print(csv_list)
    writer.writerow(csv_list)

f.close
