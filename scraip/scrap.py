from selenium import webdriver
import time
import pandas as pd
import re
import datetime
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from .models import reviews




def get():
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    
    driver=webdriver.Chrome("/Users/enokitoshiki/anaconda3/envs/testskyper/selenium/chromedriver", chrome_options=chrome_options)
    driver.maximize_window()
    # driver.get("https://www.jalan.net/")
    driver.get("https://www.jalan.net/yad313589/kuchikomi/")
    a = driver.find_element_by_xpath('//*[@id="contentsBody"]/div[2]/div/ul/li[1]/dl/dd/span').text
    b = driver.find_element_by_xpath('//*[@id="contentsBody"]/div[2]/div/ul/li[2]/dl/dd/span').text
    c = float(b)
    print(c)
    print("完了")
    row = reviews(text=a, total_review=c)
    row.save()
    
    
if __name__ == '__main__':
    get()
    
    
    
    