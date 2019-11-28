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

url = "https://jp.reuters.com/investing"
proc_ts = datetime.datetime.now()

html = urllib.request.urlopen(url)

soup = BeautifulSoup(html, "html.parser")

tbls = soup.find_all('table', class_='dataTable')

mkt_hash = {}

for tbl in tbls:
    for tr in tbl.find_all('tr'):
        td = tr.find_all('td')
        if len(td) > 2:
            mkt_hash[td[0].text.strip()] = td[1].text.strip().replace(',','')

for mkt_data in mkt_hash:
    csv_list = []
    csv_list.append(mkt_data)
    csv_list.append(str(proc_ts))
    csv_list.append(mkt_hash[mkt_data])
    csv_list.append(url)
    csv_list.append(str(proc_ts))

    print(csv_list)
    if f_open:
        writer.writerow(csv_list)

if f_open:
    f.close
