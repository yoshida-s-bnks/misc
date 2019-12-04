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

url = "http://www.nikkei.com"
proc_ts = datetime.datetime.now()

html = urllib.request.urlopen(url)

soup = BeautifulSoup(html, "html.parser")
uls = soup.find_all('ul', class_='k-hub-market__content')

for ul_tag in uls:
    for li_tag in ul_tag.find_all('li', class_='k-hub-market__index'):
        csv_list = []
        csv_list.append(li_tag.find('span').previousSibling)
        data_ts = str(proc_ts.year) +'-'+ li_tag.find('a').get('title').strip(' ''前引''大引’’終値').replace('月','-').replace('日','')
        csv_list.append(data_ts)
        csv_list.append(li_tag.find('span', class_='k-hub-market__current-price').text.replace(',',''))
        csv_list.append(url)
        csv_list.append(str(proc_ts))

        print(csv_list)
        if f_open:
            writer.writerow(csv_list)

if f_open:
    f.close
