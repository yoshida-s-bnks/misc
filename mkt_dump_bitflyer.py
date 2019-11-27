import urllib.request, urllib.error
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import datetime
import sys
import csv
import os

url = "https://bitflyer.com/ja-jp/"
proc_ts = datetime.datetime.now()

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
driver.get(url)

html = driver.page_source.encode('utf-8')

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
div_ = soup.find('div', class_='bf-bcprice')
print (div_.prettify())
b_ask = float(div_.find('span', class_='js-lastask').text.replace(',',''))
b_bid = float(div_.find('span', class_='js-lastbid').text.replace(',',''))

b_mid = (b_ask + b_bid) / 2

csv_list = []
csv_list.append('ビットコイン円')
csv_list.append(str(proc_ts))
csv_list.append(b_mid)
csv_list.append(url)
csv_list.append(str(proc_ts))

print (csv_list)
if logger:
    writer.writerow(csv_list)
    f.close
