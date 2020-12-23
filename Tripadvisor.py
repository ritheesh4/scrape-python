#!/usr/bin/env python
# coding: utf-8

# In[137]:


from bs4 import BeautifulSoup
import urllib
import re
list1 = []
html_page = urllib.request.urlopen("https://www.tripadvisor.in/Restaurants-g293916-zfn15620322-Bangkok.html#EATERY_OVERVIEW_BOX")
soup = BeautifulSoup(html_page)
for link in soup.findAll('a'):
    x = link.get('href')
    if x is not None:
        if 'Restaurant_Review' in x:
            print(x)
            list1.append(x)


# In[138]:


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


# In[139]:


SEARCH_PAGE_URL = "https://www.tripadvisor.in/Restaurants-g293916-zfn15620322-Bangkok.html#EATERY_OVERVIEW_BOX"
#pageContent = requests.get(SEARCH_PAGE_URL).text
#soup = BeautifulSoup(pageContent,"html.parser")


# In[140]:


chromedriver = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chromedriver)
driver.get(SEARCH_PAGE_URL)


# In[141]:


list1 = []
i =0
links = driver.find_elements_by_tag_name('a')
print(i)
# print(links)
for link in links:
    #wait.until(ExpectedConditions.presenceOfElementLocated(By.id("whatever elemnt")))
    x = link.get_attribute('href')
    if x is not None:
        if 'Restaurant_Review' in x:
            list1.append(x)
time.sleep(2)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1000);")
driver.find_element_by_xpath('//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/a').click()
time.sleep(5)

    
while i <2:
    links = driver.find_elements_by_tag_name('a')
    # print(i)
    # print('Inside while loop')
    # print(links)
    for link in links:
        #wait.until(ExpectedConditions.presenceOfElementLocated(By.id("whatever elemnt")))
        x = link.get_attribute('href')
        if x is not None:
            if 'Restaurant_Review' in x:
                list1.append(x)
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1000);")
    try:
        driver.find_element_by_xpath('//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/a[2]').click()
    except:
        print("")
    time.sleep(5)
    
    i += 1


# In[142]:


list1 = list(set(list1))
list2 = [x for x in list1 if '#REVIEWS' not in x]
len(list2)


# In[144]:


import scrape
import os
df1 = pd.DataFrame(columns = ['restaurant_name', 'ratings', 'review', 'location'])
for i in range(len(list1)):
    try:
        html_page = urllib.request.urlopen(list2[i])
    except:
        print("")
    soup = BeautifulSoup(html_page)
    df = {}
    try:
        df['restaurant_name'] = soup.find('h1',{'class':'_3a1XQ88S'}).text
    except: df['restaurant_name'] = ''
    print(df['restaurant_name'])
    try:
        ratingString = soup.find('svg',{'class':'_3KcXyP0F'})['title']
        if '-1.' == ratingString[:3]:
            df['ratings'] = '0'            
        else:
            df['ratings'] = ratingString[:3]
        
    except:
        df['ratings'] = 0
    try:
        df['review']=soup.find('a',{'class':'_3S6pHEQs'}).text
    except:
        df['review'] = ''
    try:
        df['location']=soup.find('span',{'class':'_2saB_OSe'}).text
    except:
        df['location'] = ''
    df1 =df1.append(df, ignore_index=True)
    print(df1)


# In[145]:


df1.to_csv("Tripadvisor_thonburi.csv")


# In[124]:


df1.shape


# In[ ]:




