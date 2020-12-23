#!/usr/bin/env python
# coding: utf-8

# In[33]:


import pandas as pd
import numpy as np


# In[47]:


data = pd.read_csv("C:\\Users\\trasto02\\Documents\\Coca Cola\\FP+TA.csv")


# In[48]:


print(data.head(10))


# In[49]:


data.shape


# In[50]:


data = data.reset_index()


# In[51]:


print(data.iloc[100,:])


# In[52]:


from googletrans import Translator


# In[53]:


translator = Translator()
translator.translate("เดอะมอลล์ ", dest = "en").text

data = data.dropna(subset = ['restaurant_name'])


# In[54]:


translatedList = []
from langdetect import detect

print(detect("เดอะมอลล์ ท่าพระ, ชั้น B ใกล้ธนาคารธนชาติ"))
for index, row in data.iterrows():

    lang = detect(row['restaurant_name'])
    print(lang)
    if lang == "th":
        print(row['restaurant_name'])
        # REINITIALIZE THE API
        translator = Translator()
        newrow = row.copy()
        try:
            # translate the 'text' column
            translated = translator.translate(row['restaurant_name'], dest='en')
            newrow['translated'] = translated.text
            print(newrow['translated'])
            data.loc[index, 'restaurant_name'] = newrow['translated']
        except Exception as e:
            print(str(e))
            continue


# In[62]:


translatedList = []
from langdetect import detect
import time

print(detect("เดอะมอลล์ ท่าพระ, ชั้น B ใกล้ธนาคารธนชาติ"))
for index, row in data.iterrows():

    lang = detect(row['location'])
    print(lang)
    if lang == "th":
        print(row['location'])
        # REINITIALIZE THE API
        time.sleep(2)
        translator = Translator()
        newrow = row.copy()
        try:
            # translate the 'text' column
            translated = translator.translate(row['location'], dest='en')
            newrow['translated'] = translated.text
            print(newrow['translated'])
            data.loc[index, 'location'] = newrow['translated']
        except Exception as e:
            print(str(e))
            continue


# In[64]:


data.iloc[1341,4]


# In[63]:


translator = Translator()
translator.translate(data.iloc[100,4]).text


# In[65]:


data.to_excel("Final_1.xlsx")


# In[ ]:




