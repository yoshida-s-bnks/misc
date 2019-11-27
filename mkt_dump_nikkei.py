import urllib.request, urllib.error
from bs4 import BeautifulSoup
import datetime
import sys
import csv
import os

url = "http://www.nikkei.com"
proc_ts = datetime.datetime.now()

html = urllib.request.urlopen(url)

try:
    f = open(sys.argv[1],'a')
    print ("##logfile: " + sys.argv[1])
    writer = csv.writer(f)
    logger = True
except IndexError:
    print ("**logfile: no file name provided, skipping logfile.")
    logger = False
except:
    print ("**logfile: failed to open " + sys.argv[1])
    logger = False

soup = BeautifulSoup(html, "html.parser")
uls = soup.find_all('ul', class_='k-hub-market__content')

for ul_tag in uls:
    for li_tag in ul_tag.find_all('li', class_='k-hub-market__index'):
        csv_list = []
        csv_list.append(li_tag.find('span').previousSibling)
        data_ts = str(proc_ts.year) +'-'+ li_tag.find('a').get('title').strip(' ''大引’’終値').replace('月','-').replace('日','')
        csv_list.append(data_ts)
        csv_list.append(li_tag.find('span', class_='k-hub-market__current-price').text.replace(',',''))
        csv_list.append(url)
        csv_list.append(str(proc_ts))

        print(csv_list)
        if logger:
            writer.writerow(csv_list)

if logger:
    f.close
