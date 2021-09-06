import keyring
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import chromedriver_binary


slots = []

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

driver.get("https://shibuya-yoyaku.seagull-lc.com/shibuya-web/reserve/gin_menu")

driver.find_element_by_name("RiyosyaForm").click()
driver.find_element_by_name("RiyosyaForm").click()

uid = sys.argv[1]
pwd = sys.argv[2]
driver.find_element_by_name("g_riyoushabangou").send_keys(uid)
driver.find_element_by_name("ansyono").send_keys(pwd)
driver.find_element_by_name("ansyono").send_keys(Keys.ENTER)

driver.find_element_by_name("YykForm").click()
driver.find_element_by_id("button4").click()
driver.find_element_by_partial_link_text("バレーボール").click()
driver.find_element_by_partial_link_text("ひがし健康プラザ").click()
driver.find_element_by_id("button1").click()
driver.find_element_by_id("btnOK").click()

el = True
while(el):
    element = driver.find_element_by_xpath("//*[@id=\"timetable\"]/ul/li[5]/a/img")
    day = driver.find_element_by_class_name("day").text
    # try:
    #     flag = driver.find_element_by_xpath("//*[@id=\"button0_8\"]")
    #     slots.append(day + "16:30-18:30")
    #     print(day + "16:30-18:30")
    # except:
    #     pass
    try:
        flag = driver.find_element_by_xpath("//*[@id=\"button0_10\"]")
        slots.append(day + "19:00-21:00")
        print(day + "19:00-21:00")
    except:
        pass
    try:
        element.click()
    except Exception as e:
        el = False

if(len(slots) == 0):
    print("空きなし")
# print(slots)
