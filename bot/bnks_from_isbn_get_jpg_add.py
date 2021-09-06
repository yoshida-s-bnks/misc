from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

from bs4 import BeautifulSoup

options = Options()
options.headless = True

driver = webdriver.Chrome(options=options)

isbns = [9784866511634,
9784866513171,
9784866513454,
9784866511641,
9784866513461,
9784866513478
]

try:
    for isbn in isbns:
        driver.get("https://bunkyosha.com/books/"+str(isbn))
        url = driver.find_element_by_xpath("/html/body/div/main/div/div/div[1]/div[1]/figure/img").get_attribute("src")

        print(str(isbn) + "," + url)

    driver.close()
except Exception as e:
    print(e)
