import urllib.request, urllib.error
from bs4 import BeautifulSoup
import datetime
import sys
import csv
import os

url = "http://gold.tanaka.co.jp/index.php"
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
div_ = soup.find('div', id='soba_info')
data_ts = div_.find('p', id='release_time').text.strip('公表').replace('/','-')

for li_tag in div_.find_all('li'):
    csv_list = []
    csv_list.append(li_tag.find('span').previousSibling)
    csv_list.append(data_ts)
    csv_list.append(li_tag.find('br').previousSibling.strip('円').replace(',',''))
    csv_list.append(url)
    csv_list.append(str(proc_ts))

    print(csv_list)
    if logger:
        writer.writerow(csv_list)

if logger:
    f.close
