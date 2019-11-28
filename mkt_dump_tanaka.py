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
    if f_open:
        writer.writerow(csv_list)

if f_open:
    f.close
