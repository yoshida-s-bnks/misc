from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from bs4 import BeautifulSoup
import datetime
import optparse
import csv

########################################
# open output file if passed in from argument
# if it fails to open, or not provided, f_open flag is set to false
parser = optparse.OptionParser()

parser.add_option('-o', '--output', dest="output_filename", default="")

options, remainder = parser.parse_args()

try:
    f = open(options.output_filename, 'a+')
    print ("##output file: " + options.output_filename)
    writer = csv.writer(f)
    f_open = True
except:
    print ("**output file: failed to open " + options.output_filename)
    f_open = False
########################################

url = "https://bitflyer.com/ja-jp/"
proc_ts = datetime.datetime.now()

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
driver.get(url)

html = driver.page_source.encode('utf-8')

soup = BeautifulSoup(html, "html.parser")
div_ = soup.find('div', class_='bf-bcprice')

b_ask = float(div_.find('span', class_='js-lastask').text.replace(',',''))
b_bid = float(div_.find('span', class_='js-lastbid').text.replace(',',''))

b_mid = (b_ask + b_bid) / 2

csv_list = []
csv_list.append('BTC-JPY')
csv_list.append(str(proc_ts))
csv_list.append(b_mid)
csv_list.append(url)
csv_list.append(str(proc_ts))

print (csv_list)
if f_open:
    writer.writerow(csv_list)
    f.close
