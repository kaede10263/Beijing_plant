from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import re
import os

def check_date():
    dir_list = os.listdir(dir_path)
    return len(dir_list)

def open_browser():
    browser = webdriver.Chrome()
    browser.implicitly_wait(5)
    browser.get(url)
    
    time.sleep(5)

    return browser

def login():
    try:
        browser.find_element_by_xpath("//*[contains(text(), '登入')]").click()

        time.sleep(1)

        user = browser.find_element_by_xpath("//input[@type='email']")
        user.send_keys("kaede10263@icloud.com")
        password = browser.find_element_by_xpath("//input[@type='password']")
        password.send_keys("Waynesu0")
        
        login = browser.find_elements_by_xpath("//*[contains(text(), '登入')]")
        login[-1].click()

        time.sleep(3)

    except:
        print("error")
        browser.quit()

def download_file(day):
    while(day):
        target_day_url = url_prefix + str(day)
        browser.get(target_day_url)
        unopen = browser.find_elements_by_xpath("//*[contains(text(), '題目尚未釋放')]")
        if(unopen):
            break
        else:
            soup = BeautifulSoup(browser.page_source, 'lxml')
            a_element = soup.find("a", {'href':re.compile("//pycrawler-fileentity.*")})
            #print("a_element",a_element)

            pdfURL = a_element['href']
            pdfURL = "https:" + pdfURL

            r = requests.get(pdfURL, stream=True)
            select_day = 'D' + str(day)
            select_day = "//*[contains(text(), 'D%s')]"%(day)
            print(select_day)
            
            DirName = browser.find_elements_by_xpath(select_day)[1].text
            if "/" in DirName:
                DirName = DirName.replace("/","-")
            #DirName = "D" + str(day)
            print("DirName",DirName)
            fileName = DirName + ".pdf"
            Dir = os.path.join(dir_path, DirName)
            fileName = os.path.join(Dir, fileName)
            os.makedirs(Dir, exist_ok=True)

            with open(fileName, 'wb') as f:
                f.write(r.content)

            hwURL = hwURL_prefix + DirName
            hw_name = DirName + ".7z"
            hw = os.path.join(Dir, hw_name)

            r = requests.get(hwURL, stream=True)
            with open(hw, 'wb') as f:
                f.write(r.content)

        day += 1
    
dir_path = "D://GDbackup/cupoy/1st-PyCrawlerMarathon_data"
day = "1"
url_prefix = "https://pycrawler.cupoy.com/mission/D"
hwURL_prefix = "https://pycrawler.cupoy.com/HomeworkAction.do?op=getHomeworkFileComb&hwid="
url = url_prefix + day

browser = open_browser()
login()

day = check_date()
download_file(day)

print("finish")

browser.quit()
