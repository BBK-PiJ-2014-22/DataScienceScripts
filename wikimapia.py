# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 09:50:24 2016

Scraping information on Public Social Housing Estates from WikiMapia

@author: Jamie
"""

#import GeoPy
import requests
#import json
#import shapefile

AREA = {'UK': {'lat_min': 49.871159
              ,'lat_max': 55.811741
              ,'lon_min': -6.37988
              ,'lon_max': 1.76896}
              
       ,'London' : {'lat_min': 51.28
                   ,'lat_max': 51.686
                   ,'lon_min': -0.489
                   ,'lon_max':0.236}
       }       


def getWMData(categories, apiKey, page=1, file_format='json', area = 'UK'):
    '''Gets a full list of all search entries for a WikiMapia category'''
    
    area = getArea(area)
    
    wmurl = 'http://api.wikimapia.org/'
    params = { 'key'      : apiKey
              ,'function' : 'place.Getbyarea'
              ,'format'   : file_format
              ,'count'    : 100
              ,'page'     : page
              ,'coordsby' : 'latlon'
              ,'lon_min'  : area['lon_min']
              ,'lon_max'  : area['lon_max']
              ,'lat_min'  : area['lat_min']
              ,'lat_max'  : area['lat_max']
              ,'category_or' : categories}
              
    #Adds categories of interest to the query
    #Not needed unless I need a category keyword....
#    try:
#        if not isinstance(categories, str):
#            params['category'] = categories[0]
#            params['category_or'] = list(categories[1:])
#        else:
#            params['category'] = categories
#    except TypeError:
#        raise TypeError('Categories must be a str or iterable list-like object')

    response = requests.get(wmurl, params)
    response.raise_for_status() 
    return response
#    result = response.json()
    
    #Recursive call to get around the page limit of 100 results
#    if len(result) == 100:
#        result += getWMData(categories, apiKey, page+1, file_format)    

 #   return result  

def getArea(area):
    return AREA[area]
    
def getRegions():
    url = 'http://maps.communities.gov.uk/geoserver/ows'
    params = { 'service'      : 'WFS'
              ,'version'      : '2.0.0'
              ,'request'      : 'GetFeature'
              ,'typeName'     : 'admingeo:EER_DEC_2013_GB_WGS84'
              ,'outputFormat' : 'json'
              ,'propertyname' : 'EER13CD,EER13NM'
             }
    return requests.get(url, params)

def getRegionBoundaries(region_code):
    url = 'http://maps.communities.gov.uk/geoserver/admingeo/ows'
    params = { 'service'      : 'WFS'
              ,'version'      : '1.0.0'
              ,'request'      : 'GetFeature'
              ,'typeName'     : 'admingeo:EER_DEC_2013_GB_WGS84'
              ,'outputFormat' : 'json'
              ,'cql_filter'   :  'EER13CD='+region_code
             }
    return requests.get(url, params)
    
    
 