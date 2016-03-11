# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 09:50:24 2016

Scraping information on Public Social Housing Estates from WikiMapia

@author: Jamie
"""

import ScraperWiki
import GeoPy
import requests
import json
import shapefile

def getWMData_Category(categories, apiKey, page=1, file_format='json'):
    '''Gets a full list of all search entries for a WikiMapia category'''
    
    wmurl = 'http://api.wikimapia.org/'
    params = { 'key'      : apiKey
              ,'function' : 'place.search'
              ,'format'   : file_format
              ,'count'    : 100
              ,'page'     : page
              ,'categories_or' : categories}
              
    #Adds categories of interest to the query
     '''Not needed unless I need a categories....
    try:
        if not isinstance(categories, str):
            params[category] = categories[0]
            params[category_or] = list(categories[1:])
        else:
            params[category] = categories
    except TypeError:
        raise TypeError('Categories must be a str or iterable list-like object')'''

    response = requests.get(wmurl, params)
    response.raise_for_status() 
    result = response.json()
    
    #Recursive call to get around the page limit of 100 results
    if len(result) == 100:
        result += getWMData_category(categories, apiKey, page+1, file_format)    

    return result  


w = shapefile.Wrier



