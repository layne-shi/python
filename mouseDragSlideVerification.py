from selenium import webdriver
from selenium.webdriver import ActionChains
import time

browser = webdriver.Chrome()

browser.get('https://www.haozu.com/bj/house1518447/')

action = ActionChains(browser)
 
source = browser.find_element_by_id("nc_1_n1z")#需要滑动的元素
action.drag_and_drop_by_offset(source, 258,0).perform()

time.sleep(500000)
