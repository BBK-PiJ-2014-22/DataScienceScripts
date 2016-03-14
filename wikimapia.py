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
                   ,'lon_max': 0.236}
       }       


def getWMData(category, apiKey, page=1, file_format='json', area = 'UK'):
    '''Gets a list of all proprties in an area for a WikiMapia category

TODO: multiple category support
TODO: spool through regions over a certain size
    '''
    
    box = getArea(area)
    
    wmurl = 'http://api.wikimapia.org/'
    params = { 'key'      : apiKey
              ,'function' : 'place.Getbyarea'
              ,'format'   : file_format
              ,'count'    : 100
              ,'page'     : page
              ,'coordsby' : 'latlon'
              ,'lon_min'  : box['lon_min']
              ,'lon_max'  : box['lon_max']
              ,'lat_min'  : box['lat_min']
              ,'lat_max'  : box['lat_max']
              ,'category' : category}
              
    response = requests.get(wmurl, params)
    places = response.json()['places']
    result = {k['id']:k for k in places}
    
    #Recursive call to get around the page limit of 100 results
    if len(result) == 100:
        result.update(getWMData(category, apiKey, page+1, file_format, area))
    
    return result  

def getArea(area):
    '''Temporary function for accessing different areas'''
    return AREA[area]
    
def getRegions():
    '''Returns a dictionary of regions, with ID, EER13CD ID code and description'''
    url = 'http://maps.communities.gov.uk/geoserver/ows'
    params = { 'service'      : 'WFS'
              ,'version'      : '2.0.0'
              ,'request'      : 'GetFeature'
              ,'typeName'     : 'admingeo:EER_DEC_2013_GB_WGS84'
              ,'outputFormat' : 'json'
              ,'propertyname' : 'EER13CD,EER13NM'
             }
    result = requests.get(url, params).json()
    return {k['id']:k['properties'] for k in result['features']}


#var thisRegCode = rList[thisPos];
#var thisRegBoundsURL = 'http://maps.communities.gov.uk/geoserver/admingeo/ows?service=WFS&version=1.0.0';
#thisRegBoundsURL += '&request=GetFeature&typeName=admingeo:EER_DEC_2013_GB_WGS84';
#thisRegBoundsURL += '&outputFormat=text/javascript&cql_filter=EER13CD=%27' +  thisRegCode + '%27';


def getRegionBoundaries(region_code):
    '''Access the boundaries of a given region code from the geoserver
    
    Will return as a list of lon/lat coordinates in list'''
    url = 'http://maps.communities.gov.uk/geoserver/admingeo/ows'
    params = { 'service'      : 'WFS'
              ,'version'      : '1.0.0'
              ,'request'      : 'GetFeature'
              ,'typeName'     : 'admingeo:EER_DEC_2013_GB_WGS84'
              ,'outputFormat' : 'json'
              ,'cql_filter'   :  "EER13CD='"+region_code+"'"
             }
    #As region code is unique there can only be one result in the features list
    response = requests.get(url, params).json()['features'][0]
    list_coords = response['geometry']['coordinates'] 
    #list_coords is returning a list of lists with 1 member which is a list 
    #of lists of coords
    #The below code converts this to a single list and must be 
    
    #This is non-Pythonic but a lot more understandable than a list comp
    #TODO - Refactor and check assumption on geography
    result = []
    for j in list_coords:
        sl = j[0]
        for i in sl:
            result.append(i)
    return result

def getBBox(coordinates, lon_key=0, lat_key=1):
    '''Returns a dict with min and max lat and lon coords 
 
    lon_key and lat_key represent the key required to extract lat and lon from
    the list of coordinates. The default assumes it is a possitional data structure
    (e.g. tuple, list) in lon/lat order. If they are in reverse order switching 
    the positions will parse correctly. Alternatively, if a dict structure is used
    then simply enter the correct keys.'''
 
    lon = [i[0] for i in coordinates[0]]   
    lat = [i for i in coordinates[1]]
    
    return {'lat_min': min(lat)
           ,'lat_max': max(lat)
           ,'lon_min': min(lon)
           ,'lon_max': max(lon)
           }
    
    
 