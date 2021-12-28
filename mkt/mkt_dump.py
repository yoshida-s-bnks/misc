from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import socket
from bs4 import BeautifulSoup
import datetime
import optparse
import csv
import os, time

def __get_interval():
    return datetime.timedelta(hours=3.6)

def __get_html(url, verbose=False):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    if verbose:
        print("##opening " + url)
    driver.get(url)

    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")

    if verbose:
        print("##closing driver")
    socket.setdefaulttimeout(5)
    try:
       driver.quit()
    except:
       None
    finally:
       # Set to something higher you want
       socket.setdefaulttimeout(60)

    return soup

def scr_nikkei(lines=[], verbose=False):
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

def scr_tanaka(lines=[], verbose=False):
    url = "http://gold.tanaka.co.jp/index.php"

    soup = __get_html(url,verbose)
    proc_ts = datetime.datetime.now()

    div_ = soup.find('div', class_='soba_info')
    data_ts = div_.find('p', class_='release_time').text.strip('公表').replace('/','-')


    metal = ['金','プラチナ','銀']
    l = []
    for item in div_.find_all('td', class_='price_sell'):
        p = item.find('span', class_='price_num')
        if(p != None):
            # print(p.text.replace(',',''))
            line = []
            line.append(metal.pop(0))
            line.append(data_ts)
            line.append(p.text.replace(',',''))
            line.append(url)
            line.append(str(proc_ts))
            l.append(line)

    if verbose:
        print('##%d record(s) found.' % len(l))
    lines.extend(l)
    return lines


def scr_reuters(lines=[], verbose=False):
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

def scr_bitflyer(lines=[], verbose=False):
    url = "https://bitflyer.com/ja-jp/bitcoin-chart"

    soup = __get_html(url, verbose)
    proc_ts = datetime.datetime.now()

    b_mid = soup.find('div',class_='p-currencyInfo__price').text.strip().replace(',','').split('※')[0]
    print(b_mid)

    line = []
    line.append('BTC-JPY')
    line.append(str(proc_ts))
    line.append(b_mid)
    line.append(url)
    line.append(str(proc_ts))
    lines.append(line)
    return lines

def scr_bus_insider_btc(lines=[], verbose=False):
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
    parser.add_option('-v', '--verbose', action="store_true")
    parser.add_option('-f', '--force', action="store_true")
    parser.add_option('-a', '--all', action="store_true")
    parser.add_option('-n', '--nikkei', action="store_true")
    parser.add_option('-t', '--tanaka', action="store_true")
    parser.add_option('-b', '--bitflyer', action="store_true")
    parser.add_option('-r', '--reuters', action="store_true")

    options, remainder = parser.parse_args()

    if options.force:
        f_open = True
    else:
        f_open = False
        try:
            mod_t = time.localtime(os.path.getmtime(options.output_filename))
            mod_ts = datetime.datetime(*mod_t[:6])
            proc_ts = datetime.datetime.now()
            print ("##output file: last modified %s" % time.strftime('%Y-%m-%d %H:%M:%S', mod_t))

            if mod_ts < proc_ts - __get_interval():
                f_open = True
                if options.verbose:
                    print("##outpuf file: %.1f hours passed since last modified. appending result." % (__get_interval().seconds / 3600))
            else:
                if options.verbose:
                    print("**outpuf file: %.1f hours hasn't passed. skip appending." % (__get_interval().seconds / 3600))
        except:
            f_open = True
            if options.verbose:
                print ("**output file: new file? failed to obtain last modified time.")

    if f_open:
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

    if (options.all or options.nikkei):
        lines = scr_nikkei(lines, options.verbose)
    if (options.all or options.tanaka):
        lines = scr_tanaka(lines, options.verbose)
    if (options.all or options.bitflyer):
        lines = scr_bitflyer(lines, options.verbose)
    if (options.all or options.reuters):
        lines = scr_reuters(lines, options.verbose)
    # lines = scr_bus_insider_btc(lines, options.verbose)

    for line in lines:
        if f_open:
            writer.writerow(line)
        if options.verbose:
            print(line)

    if f_open:
        f.close
