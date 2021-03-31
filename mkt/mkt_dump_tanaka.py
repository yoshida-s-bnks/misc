import urllib.request, urllib.error
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

url = "http://gold.tanaka.co.jp/index.php"
proc_ts = datetime.datetime.now()

html = urllib.request.urlopen(url)

soup = BeautifulSoup(html, "html.parser")
# print(soup)
div_ = soup.find('div', class_='soba_info')
# print(div_)
data_ts = div_.find('p', class_='release_time').text.strip('公表').replace('/','-')
print(data_ts)
metal = ['金','プラチナ','銀']
for item in div_.find_all('td', class_='price_sell'):
    p = item.find('span', class_='price_num')
    if(p != None):
        print(p.text.replace(',',''))
        csv_list = []
        csv_list.append(metal.pop(0))
        csv_list.append(data_ts)
        csv_list.append(p.text.replace(',',''))
        csv_list.append(url)
        csv_list.append(str(proc_ts))

        print(csv_list)
        if f_open:
            writer.writerow(csv_list)
