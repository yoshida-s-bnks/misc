import urllib.request, urllib.error
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import datetime
import sys
import csv
import os

# open logger if passed in as the first argument
# if it fails to open, or not provided, logger flag is set to false
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
##########

url = "https://markets.businessinsider.com/currencies/btc-usd"
proc_ts = datetime.datetime.now()

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
driver.get(url)

html = driver.page_source.encode('utf-8')

soup = BeautifulSoup(html, "html.parser")
span = soup.find('span', class_='aktien-big-font').find('span', class_='push-data')

csv_list = []
csv_list.append('BTC-USD')
csv_list.append(str(proc_ts))
csv_list.append(span.text.replace(',',''))
csv_list.append(url)
csv_list.append(str(proc_ts))

print (csv_list)
if logger:
    writer.writerow(csv_list)
    f.close
