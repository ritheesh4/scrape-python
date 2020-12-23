#!/usr/bin/env python
# coding: utf-8

# In[2]:


from bs4 import BeautifulSoup
import urllib
import re
list1 = []
html_page = urllib.request.urlopen("https://www.foodpanda.co.th/restaurants/new?lat=13.707752314036142&lng=100.48757553386835&vertical=restaurants")
soup = BeautifulSoup(html_page)
for link in soup.findAll('a'):
    x = link.get('href')
    if x is not None:
        if 'restaurant' in x:
            print(x)
            list1.append(x)


# In[3]:


################################################
# --------- Loading libraries   -----------#####
################################################
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from itertools import chain
import xlsxwriter
import time
import sys
from lxml.html import fromstring, tostring
import pandas as pd
import numpy as np
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from openpyxl import load_workbook
import requests
import pandas as pd 
from bs4 import BeautifulSoup
import csv
from lxml import html


# In[4]:


SEARCH_PAGE_URL = "https://www.foodpanda.co.th/restaurants/lat/13.707752314036142/lng/100.48757553386835/city/Krung%20Thep%20Maha%20Nakhon/address/79%2520Somdet%2520Phra%2520Chao%2520Tak%2520Sin%2520Rd%252C%2520Khwaeng%2520Samre%252C%2520Khet%2520Thon%2520Buri%252C%2520Krung%2520Thep%2520Maha%2520Nakhon%252010600%252C%2520Thailand/Somdet%2520Phra%2520Chao%2520Tak%2520Sin%2520Road/79?postcode=Khwaeng+Samre"
#pageContent = requests.get(SEARCH_PAGE_URL).text
#soup = BeautifulSoup(pageContent,"html.parser")


# In[5]:


chromedriver = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chromedriver)
driver.get(SEARCH_PAGE_URL)


# In[30]:


list1 = []
i =0
links = driver.find_elements_by_tag_name('a')
print(i)
#print(links)
for link in links:
    #wait.until(ExpectedConditions.presenceOfElementLocated(By.id("whatever elemnt")))
    x = link.get_attribute('href')
    if x is not None:
        if 'restaurant/' in x:
            list1.append(x)
time.sleep(2)
#driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1000);")
#driver.find_element_by_xpath('//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/a').click()
time.sleep(5)

# i += 1

    
# while i <10:
#     links = driver.find_elements_by_tag_name('a')
#     print(i)
#     #print(links)
#     for link in links:
#         #wait.until(ExpectedConditions.presenceOfElementLocated(By.id("whatever elemnt")))
#         x = link.get_attribute('href')
#         if x is not None:
#             if 'restaurant' in x:
#                 list1.append(x)
#     time.sleep(2)
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1000);")
#     driver.find_element_by_xpath('//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/a[2]').click()
#     time.sleep(5)
    
#     i += 1


# In[31]:


list1 = list(set(list1))
list2 = [x.strip() for x in list1 if '#REVIEWS' not in x]
len(list2)
print(list2[0])


# In[18]:


res = requests.get("""https://www.foodpanda.co.th/restaurants/lat/13.707752314036142/lng/100.48757553386835/city/Krung%20Thep%20Maha%20Nakhon/address/79%2520Somdet%2520Phra%2520Chao%2520Tak%2520Sin%2520Rd%252C%2520Khwaeng%2520Samre%252C%2520Khet%2520Thon%2520Buri%252C%2520Krung%2520Thep%2520Maha%2520Nakhon%252010600%252C%2520Thailand/Somdet%2520Phra%2520Chao%2520Tak%2520Sin%2520Road/79?postcode=Khwaeng%20Samre""")
res.text


# In[41]:


import scrape
import os

df1 = pd.DataFrame(columns = ['restaurant_name', 'ratings', 'review', 'location', 'time'])
for i in range(0,len(list1)):
    html_page = requests.get(list2[i])
    print(list2[i], html_page)
    try:
        soup = BeautifulSoup(html_page.content)
        df = {}
        df['restaurant_name'] = soup.find('h1',{'class':'vendor-name'}).text
        print(df['restaurant_name'])
        try:
            df['ratings'] =soup.find('span',{'class':'rating'}).text
        except:
            df['ratings'] = 0
        try:
            df['review']=soup.find('span', {'class':'count'}).get("data-count")
            print(df['review'])
        except:
            df['review'] = ''
        try:
            df['location']=soup.find('p',{'class':'vendor-location'}).text
        except:
            df['location'] = ''
        try:
            df['time']=soup.find('ul',{'class':'vendor-delivery-times'}).text
        except:
            df['time'] = ''
        df1 =df1.append(df, ignore_index=True)
    except AttributeError as Exception:
        pass


# In[42]:


df1.to_csv("Foodpanda_thonburi.csv")


# In[124]:


df1.shape


# In[ ]:




