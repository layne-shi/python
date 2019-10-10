from selenium import webdriver
import time
from bs4 import BeautifulSoup


browser = webdriver.Chrome()

firstUrls = []
secondUrls = []
belongBuildDivHref = []

def getAllUrls(url, arr, pos):
    print(url)
    browser.get(url)
    print('===========')
    time.sleep(5)
    PoiResultDiv = browser.find_element_by_css_selector(".menu_area")
    aHtml = PoiResultDiv.find_element_by_css_selector(".area").get_attribute('innerHTML')    
    if pos == 1:
        aHtml = PoiResultDiv.find_element_by_css_selector(".subarea").get_attribute('innerHTML')
    
    soup = BeautifulSoup(aHtml, 'lxml')
    ahrefs = soup.select('a')
    del ahrefs[0]
    for i in ahrefs:
        arr.append(i['href'])

# 打开详情页面,并获取belong-build
def listCon(url):    
    print(url)
    browser.get(url)
    print('===listCon========')
    time.sleep(5)
    js_="document.getElementsByClassName('listCon')[0].getElementsByTagName('li')[0].getElementsByTagName('a')[0].click();"  
    browser.execute_script(js_)    
    
    browser.switch_to_window(browser.window_handles[1])
    # 获取belong-build
    belongBuildDiv = browser.find_element_by_css_selector(".belong-build").get_attribute('innerHTML')
    belongBuildDivSoup = BeautifulSoup(belongBuildDiv, 'lxml')
    belongBuildDivHref = belongBuildDivSoup.select('a')
    print(belongBuildDivHref[0]['href'])
    
    browser.close()
    browser.switch_to_window(browser.window_handles[0])

    js_="document.getElementsByClassName('listCon')[0].getElementsByTagName('li')[1].getElementsByTagName('a')[0].click();"  
    browser.execute_script(js_)    
    
    browser.switch_to_window(browser.window_handles[1])
    # 获取belong-build
    belongBuildDiv = browser.find_element_by_css_selector(".belong-build").get_attribute('innerHTML')
    belongBuildDivSoup = BeautifulSoup(belongBuildDiv, 'lxml')
    belongBuildDivHref = belongBuildDivSoup.select('a')
    print(belongBuildDivHref[0]['href'])




# 第一级
getAllUrls('https://www.haozu.com/bj/house-list/', firstUrls, 0)
# 第二级
""" for url in firstUrls:
    print('url', url)
    getAllUrls('https://www.haozu.com' + url, secondUrls, 1)

print('secondUrls', secondUrls) """

listCon('https://www.haozu.com' + firstUrls[0])

time.sleep(500)


# browser.close()

