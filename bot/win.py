import keyring

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

from bs4 import BeautifulSoup

download_dir = "/Users/yoshida.s/data/sales/win_daily/"

options = Options()
options.headless = True
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "plugins.always_open_pdf_externally": True
})

driver = webdriver.Chrome(options=options)

driver.get("https://www.winwinwin.jp/zzh/zzh")

#login
try:
    print("login...")
    uid = "BUN7464001"
    pwd = keyring.get_password("WIN",uid)
    driver.find_element_by_name("userid").send_keys(uid)
    driver.find_element_by_name("password").send_keys(pwd)
    driver.find_element_by_class_name("funcBtn").click()

    print("moving into meigara pickup...")
    driver.find_element_by_xpath("//*[@id=\"syutupansyaIchiran\"]/dl/dd/span[2]/span").send_keys(Keys.ENTER)
    print("filling the form...")
    driver.find_element_by_id("transactCode").click()
    driver.find_element_by_id("publicherCordInput").clear()
    driver.find_element_by_id("publicherCordInput").send_keys("7464")
    driver.find_element_by_id("prevDaySearch").click()
    sb = Select(driver.find_element_by_name("rank"))
    sb.select_by_visible_text("300件")

    print("hitting search...")
    driver.find_element_by_class_name("funcBtn_search").click()

    print("downloading...")
    driver.find_element_by_class_name("funcBtn_download").click()

    print("completed!")

except Exception as e:
    print(e)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")

    print(soup)
