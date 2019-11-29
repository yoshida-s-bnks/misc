from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from bs4 import BeautifulSoup
import datetime
import optparse
import csv

def __get_html(url, verbose):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    if verbose:
        print("##opening " + url)
    driver.get(url)

    html = driver.page_source.encode('utf-8')

    soup = BeautifulSoup(html, "html.parser")

    return soup

def scr_nikkei(lines, verbose):
    url = "http://www.nikkei.com"

    soup = __get_html(url,verbose)
    proc_ts = datetime.datetime.now()

    uls = soup.find_all('ul', class_='k-hub-market__content')

    l = []

    for ul_tag in uls:
        for li_tag in ul_tag.find_all('li', class_='k-hub-market__index'):
            line = []
            line.append(li_tag.find('span').previousSibling)
            data_ts = str(proc_ts.year) +'-'+ li_tag.find('a').get('title').strip(' ''前引''大引’’終値').replace('月','-').replace('日','')
            line.append(data_ts)
            line.append(li_tag.find('span', class_='k-hub-market__current-price').text.replace(',',''))
            line.append(url)
            line.append(str(proc_ts))
            l.append(line)
    if verbose:
        print('##%d record(s) found.' % len(l))
    lines.extend(l)
    return lines

def scr_tanaka(lines, verbose):
    url = "http://gold.tanaka.co.jp/index.php"

    soup = __get_html(url,verbose)
    proc_ts = datetime.datetime.now()

    div_ = soup.find('div', id='soba_info')
    data_ts = div_.find('p', id='release_time').text.strip('公表').replace('/','-')

    l = []
    for li_tag in div_.find_all('li'):
        line = []
        line.append(li_tag.find('span').previousSibling)
        line.append(data_ts)
        line.append(li_tag.find('br').previousSibling.strip('円').replace(',',''))
        line.append(url)
        line.append(str(proc_ts))
        l.append(line)
    if verbose:
        print('##%d record(s) found.' % len(l))
    lines.extend(l)
    return lines

def scr_reuters(lines, verbose):
    url = "https://jp.reuters.com/investing"

    soup = __get_html(url, verbose)
    proc_ts = datetime.datetime.now()

    tbls = soup.find_all('table', class_='dataTable')

    mkt_hash = {}

    for tbl in tbls:
        for tr in tbl.find_all('tr'):
            td = tr.find_all('td')
            if len(td) > 2:
                mkt_hash[td[0].text.strip()] = td[1].text.strip().replace(',','')

    l = []
    for mkt_data in mkt_hash:
        line = []
        line.append(mkt_data)
        line.append(str(proc_ts))
        line.append(mkt_hash[mkt_data])
        line.append(url)
        line.append(str(proc_ts))
        l.append(line)

    if verbose:
        print('##%d record(s) found.' % len(l))
    lines.extend(l)
    return lines

def scr_bitflyer(lines, verbose):
    url = "https://bitflyer.com/ja-jp/"

    soup = __get_html(url, verbose)
    proc_ts = datetime.datetime.now()

    div_ = soup.find('div', class_='bf-bcprice')

    b_ask = float(div_.find('span', class_='js-lastask').text.replace(',',''))
    b_bid = float(div_.find('span', class_='js-lastbid').text.replace(',',''))

    b_mid = (b_ask + b_bid) / 2

    line = []
    line.append('BTC-JPY')
    line.append(str(proc_ts))
    line.append(b_mid)
    line.append(url)
    line.append(str(proc_ts))
    lines.append(line)
    return lines

def scr_bus_insider_btc(lines, verbose):
    url = "https://markets.businessinsider.com/currencies/btc-usd"

    soup = __get_html(url, verbose)
    proc_ts = datetime.datetime.now()

    span = soup.find('span', class_='aktien-big-font').find('span', class_='push-data')

    line = []
    line.append('BTC-USD')
    line.append(str(proc_ts))
    line.append(span.text.replace(',',''))
    line.append(url)
    line.append(str(proc_ts))
    lines.append(line)
    return lines


if __name__ == '__main__':
    ########################################
    # open output file if passed in from argument
    # if it fails to open, or not provided, f_open flag is set to false
    parser = optparse.OptionParser()

    parser.add_option('-o', '--output', dest="output_filename", default="")
    parser.add_option('-v', '--verbose',action="store_true")

    options, remainder = parser.parse_args()

    try:
        f = open(options.output_filename, 'a+')
        if options.verbose:
            print ("##output file: " + options.output_filename)
        writer = csv.writer(f)
        f_open = True
    except:
        if options.verbose:
            print ("**output file: failed to open " + options.output_filename)
        f_open = False
    ########################################

    lines = []
    lines = scr_nikkei(lines, options.verbose)
    lines = scr_tanaka(lines, options.verbose)
    lines = scr_reuters(lines, options.verbose)
    lines = scr_bitflyer(lines, options.verbose)
    lines = scr_bus_insider_btc(lines, options.verbose)

    for line in lines:
        if f_open:
            writer.writerow(line)
        if options.verbose:
            print(line)

    if f_open:
        f.close
