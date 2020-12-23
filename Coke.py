#!/usr/bin/env python
# coding: utf-8

# In[1]:


with open('apikey.txt') as f:
    api_key = f.readline()
    f.close


# In[2]:


import gmaps
# print(api_key)
gmaps.configure(api_key='AIzaSyAcJDCrpeCB1ivQJAc8DObHrCp5snrRBjs')


# In[3]:


new_york_coordinates = (13.736717, 100.523186)
gmaps.figure(center=new_york_coordinates, zoom_level=11)


# In[41]:


import requests
import json
import time


class GooglePlaces(object):
    def __init__(self, apiKey):
        super(GooglePlaces, self).__init__()
        self.apiKey = apiKey
 
    def search_places_by_coordinate(self, location, radius, types):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places = []
        params = {
            'location': location,
            'radius': radius,
            'types': types,
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        results =  json.loads(res.content)
        places.extend(results['results'])
        time.sleep(2)
        while "next_page_token" in results:
            params['pagetoken'] = results['next_page_token'],
            res = requests.get(endpoint_url, params = params)
            results = json.loads(res.content)
            places.extend(results['results'])
            time.sleep(2)
        return places
 
    def get_place_details(self, place_id, fields):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'placeid': place_id,
            'fields': ",".join(fields),
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        place_details =  json.loads(res.content)
        return place_details


# In[6]:


api = GooglePlaces("AIzaSyAcJDCrpeCB1ivQJAc8DObHrCp5snrRBjs")


# In[42]:


data_district = pd.read_excel("C:\\Users\\trasto02\\Documents\\Coca Cola\\District_coordinates.xlsx", encoding = 'latin-1')


# In[76]:


import math

R = 6378.1 #Radius of the Earth
brng = 3.14 #Bearing is 90 degrees converted to radians.
d = 1 #Distance in km

#lat2  52.20444 - the lat result I'm hoping for
#lon2  0.36056 - the long result I'm hoping for.

lat1 = math.radians(13.712429) #Current lat point converted to radians
lon1 = math.radians(100.483355) #Current long point converted to radians

lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
     math.cos(lat1)*math.sin(d/R)*math.cos(brng))

lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
             math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

lat2 = math.degrees(lat2)
lon2 = math.degrees(lon2)

print(lat2)
print(lon2)


# In[80]:


br = [0, 1.57, 2.35, 3.14, 4.71]
ll = []
for brng in br:
    lat1 = math.radians(13.712429) #Current lat point converted to radians
    lon1 = math.radians(100.483355) #Current long point converted to radians

    lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
         math.cos(lat1)*math.sin(d/R)*math.cos(brng))

    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
                 math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    ll.append(str(lat2) + "," + str(lon2)) 
print(ll)


# In[84]:


place_types = ['restaurant', 'department_store', 'convenience_store', 'bar', 'cafe', 'lodging', 'meal_delivery', 'meal_takeaway', 
               'shopping_mall' , 'supermarket']
supermarket_final = pd.DataFrame(columns = ['geometry', 'icon', 'id', 'name', 'opening_hours', 'photos', 'place_id',
           'plus_code', 'price_level', 'rating', 'reference', 'scope', 'types',
           'user_ratings_total', 'vicinity'])
for plac in place_types:
    for l in ll:
        restaurant = api.search_places_by_coordinate(l, "1000", plac)
        print(len(restaurant))
        df_dep_store = pd.DataFrame(restaurant)
        df_dep_store['Place_type'] = plac
        print(df_dep_store.head())
        supermarket_final = supermarket_final.append(df_dep_store, ignore_index = True)
supermarket_final.to_csv("data_final_thanburi.csv")


# In[ ]:


restaurant = api.search_places_by_coordinate("13.725, 100.485833" , "10000", "supermarket")
print(len(restaurant))
df_dep_store = pd.DataFrame(restaurant)
supermarket_final = supermarket_final.append(df_dep_store, ignore_index = True)


# In[62]:


malls_final.to_csv('malls_final.csv')
conv_store_final.to_csv('conv_store_final.csv')
department_store_final.to_csv('department_store_final.csv')
restaurants_final.to_csv('restaurants_final.csv')
bar_final.to_csv('bar_final.csv')
cafe_final.to_csv('cafe_final.csv')
lodging_final.to_csv('lodging_final.csv')


# In[64]:


supermarket_final.to_csv('supermarket_final.csv')


# In[26]:


import pandas as pd
df_malls = pd.DataFrame(malls)


# In[37]:


print(df_malls.head())
df_malls.columns


# In[22]:


fields = ['name', 'formatted_address', 'international_phone_number', 'website', 'rating', 'review']


# In[23]:


for place in malls:
    details = api.get_place_details(place['place_id'], fields)
    try:
        website = details['result']['website']
    except KeyError:
        website = ""
 
    try:
        name = details['result']['name']
    except KeyError:
        name = ""
 
    try:
        address = details['result']['formatted_address']
    except KeyError:
        address = ""
 
    try:
        phone_number = details['result']['international_phone_number']
    except KeyError:
        phone_number = ""
 
    try:
        reviews = details['result']['reviews']
    except KeyError:
        reviews = []
    print("===================PLACE===================")
    print("Name:", name)
    print("Website:", website)
    print("Address:", address)
    print("Phone Number", phone_number)
    print("==================REVIEWS==================")
    for review in reviews:
        author_name = review['author_name']
        rating = review['rating']
        text = review['text']
        time = review['relative_time_description']
        profile_photo = review['profile_photo_url']
        print("Author Name:", author_name)
        print("Rating:", rating)
        print("Text:", text)
        print("Time:", time)
        print("Profile photo:", profile_photo)
        print("-----------------------------------------")


# In[51]:


for place in places:
    details = api.get_place_details(place['place_id'], fields)
    try:
        website = details['result']['website']
    except KeyError:
        website = ""
 
    try:
        name = details['result']['name']
    except KeyError:
        name = ""
 
    try:
        address = details['result']['formatted_address']
    except KeyError:
        address = ""
 
    try:
        phone_number = details['result']['international_phone_number']
    except KeyError:
        phone_number = ""
 
    try:
        reviews = details['result']['reviews']
    except KeyError:
        reviews = []
    print("===================PLACE===================")
    print("Name:", name)
    print("Website:", website)
    print("Address:", address)
    print("Phone Number", phone_number)
    print("==================REVIEWS==================")
    for review in reviews:
        author_name = review['author_name']
        rating = review['rating']
        text = review['text']
        time = review['relative_time_description']
        profile_photo = review['profile_photo_url']
        print("Author Name:", author_name)
        print("Rating:", rating)
        print("Text:", text)
        print("Time:", time)
        print("Profile photo:", profile_photo)
        print("-----------------------------------------")

