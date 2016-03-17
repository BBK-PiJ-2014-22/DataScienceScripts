# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 09:50:24 2016

Scraping information on Public Social Housing Estates from WikiMapia

@author: Jamie
"""

#import GeoPy
import requests
import areas
import time
#import json
#import shapefile


def getWMData(apiKey, category, page=1, file_format='json', area = 'London', key_type='EER13NM', level='region'):
    '''Gets a list of all properties in an area for a WikiMapia category

TODO: multiple category support
TODO: spool through regions over a certain size
    '''
    
    box = getArea(area, key_type, level)
    
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
                  
    while True:
        response = requests.get(wmurl, params)
        if response.status_code != 200:
            raise RuntimeError('Unknown Error in request. Response type: '+response.text )
        else:
            try:
                places = response.json()['places']
                break
            except KeyError:
                if response.json()['debug']['message'] == "IP address limit has been reached":
                    print('Waiting for IP Address request limit to reset')                
                    time.sleep(10)
                elif response.json()['debug']['code'] == 1004:
                    print('Waiting for 5 minutes for key limit to reset')                
                    time.sleep(305)
                    
                else:
                    message = 'Unknown error type from WikiMapia API: '+str(response.json())
                    raise RuntimeError(message)
                
   
    result = [k for k in places] #TODO - check if this is needed - json may be sufficient
    
    #Recursive call to get around the page limit of 100 results
    if len(result) == 100:
        result.append(getWMData(apiKey, category, page+1, file_format, area, key_type, level))
    return result  

def getArea(key, key_type='EER13NM', level='region'):
    '''Returns the bbox of the region identified by key
    
    Possible values for key_type:
    EER13NM = name of the region
    EER13CD = server ID for the region
    '''
    for i in areas.AREAS[level]:
        if i[key_type] == key:
            return i['bbox']
    raise KeyError(str(key) + ' is not a recognised key of type '+key_type+' for level '+level)
    
def getRegions():
    '''Returns a dictionary of regions, with ID, EER13CD ID code, description bbox
    
    EER13CD = region code
    EER13NM = region name description
    bbox = {lat_min, lat_max, lon_min, lon_max}
    TODO - rationalise this with counties
    '''
    url = 'http://maps.communities.gov.uk/geoserver/ows'
    params = { 'service'      : 'WFS'
              ,'version'      : '2.0.0'
              ,'request'      : 'GetFeature'
              ,'typeName'     : 'admingeo:EER_DEC_2013_GB_WGS84'
              ,'outputFormat' : 'json'
              ,'propertyname' : 'EER13CD,EER13NM'
             }
    response = requests.get(url, params).json()
    result = {k['id']:k['properties'] for k in response['features']}
    
    for i in result:
        result[i]['bbox'] = getBBox(getRegionBoundaries(result[i]['EER13CD']))
    
    return result

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
    #The below code converts this to a single list. This assumes they are polygons
    #who's sum makes up the total area. 
    
    #This is non-Pythonic but a lot more understandable than a list comp
    #TODO - Refactor and check assumption on geography. This code is horrible 
    # but necessary due to the weird data structure. 
    result = []
    for j in list_coords:
        sublist = j[0]
        for i in sublist:
            result.append(i)
    return result

def getBBox(coordinates, lon_key=0, lat_key=1):
    '''Returns a dict with min and max lat and lon coords 
 
    lon_key and lat_key represent the key required to extract lat and lon from
    the list of coordinates. The default assumes it is a possitional data structure
    (e.g. tuple, list) in lon/lat order. If they are in reverse order switching 
    the positions will parse correctly. Alternatively, if a dict structure is used
    then simply enter the correct keys.'''
 
    lon = [i[lon_key] for i in coordinates]   
    lat = [i[lat_key] for i in coordinates]
    return {'lat_min': min(lat)
           ,'lat_max': max(lat)
           ,'lon_min': min(lon)
           ,'lon_max': max(lon)
           }

def getCategory(key, category, arealevel = 'wikimapia2', areaidtype = 'wmboxid'):
    '''Gets all entries of a specific category in wikimapia'''
    arealist = areas.AREAS[arealevel]
    result = []
    for i in arealist:
        print("Getting", i[areaidtype],end=': -')
        found = getWMData(key, category, page=1, area=i[areaidtype],
                          key_type=areaidtype, level=arealevel)
        print("Found:", len(found))
        result += found
    return result
                
        
    
    
    
    
def storeFile(filelocation, result):
    '''Stores property details in a specific file''' 