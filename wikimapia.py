# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 09:50:24 2016

Scraping information on Public Social Housing Estates from WikiMapia

Importing the wikimapia library will usually take some time as a list of regions
is taken from the web and stored for use in the module. This will usually take
~30 seconds

@author: Jamie
"""

#import GeoPy
import requests
#import json
#import shapefile


def getWMData(apiKey, category, page=1, file_format='json', area = 'London'):
    '''Gets a list of all proprties in an area for a WikiMapia category

TODO: multiple category support
TODO: spool through regions over a certain size
    '''
    
    box = getArea(area, 'EER13NM')
    
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

#TODO - Rewrite to use the regions and to be able to use name or keu
def getArea(key, key_type='EER13NM'):
    '''Returns the bbox of the region identified by key
    
    Possible values for key_type:
    EER13NM = name of the region
    EER13CD = server ID for the region
    '''
    for i in regions:
        if regions[i][key_type] == key:
            return regions[i]['bbox']
    raise KeyError(key + ' is not a recognised key of type '+key_type)
    
def getRegions():
    '''Returns a dictionary of regions, with ID, EER13CD ID code, description bbox
    
    EER13CD = region code
    EER13NM = region name description
    bbox = {lat_min, lat_max, lon_min, lon_max}
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
 
    lon = [i[lon_key] for i in coordinates]   
    lat = [i[lat_key] for i in coordinates]
    return {'lat_min': min(lat)
           ,'lat_max': max(lat)
           ,'lon_min': min(lon)
           ,'lon_max': max(lon)
           }
    
#TODO - This should be replaced with the function after testing is complete
regions = {'EER_DEC_2013_GB_WGS84.1': {'EER13CD': 'E15000001',
  'EER13NM': 'North East',
  'bbox': {'lat_max': 55.81107189590653,
   'lat_min': 54.45117969612147,
   'lon_max': -0.7884184387818132,
   'lon_min': -2.689785011662573}},
 'EER_DEC_2013_GB_WGS84.10': {'EER13CD': 'S15000001',
  'EER13NM': 'Scotland',
  'bbox': {'lat_max': 60.86076144913198,
   'lat_min': 54.63323825572365,
   'lon_max': -0.7246094068773615,
   'lon_min': -8.650007166993163}},
 'EER_DEC_2013_GB_WGS84.11': {'EER13CD': 'W08000001',
  'EER13NM': 'Wales',
  'bbox': {'lat_max': 53.4356924435458,
   'lat_min': 51.37496878616603,
   'lon_max': -2.649870111344756,
   'lon_min': -5.670115637074575}},
 'EER_DEC_2013_GB_WGS84.2': {'EER13CD': 'E15000002',
  'EER13NM': 'North West',
  'bbox': {'lat_max': 55.188981362111676,
   'lat_min': 52.947149605112386,
   'lon_max': -1.9096222591042302,
   'lon_min': -3.63978108010726}},
 'EER_DEC_2013_GB_WGS84.3': {'EER13CD': 'E15000003',
  'EER13NM': 'Yorkshire and The Humber',
  'bbox': {'lat_max': 54.55945197406109,
   'lat_min': 53.301548289445854,
   'lon_max': 0.1475836647068026,
   'lon_min': -2.5647362796906266}},
 'EER_DEC_2013_GB_WGS84.4': {'EER13CD': 'E15000004',
  'EER13NM': 'East Midlands',
  'bbox': {'lat_max': 53.616366193040534,
   'lat_min': 51.977281544140624,
   'lon_max': 0.3556255856461102,
   'lon_min': -2.034087170671713}},
 'EER_DEC_2013_GB_WGS84.5': {'EER13CD': 'E15000005',
  'EER13NM': 'West Midlands',
  'bbox': {'lat_max': 53.22622396058041,
   'lat_min': 51.826078856543056,
   'lon_max': -1.1721403438198337,
   'lon_min': -3.2355407829691827}},
 'EER_DEC_2013_GB_WGS84.6': {'EER13CD': 'E15000006',
  'EER13NM': 'Eastern',
  'bbox': {'lat_max': 52.98837435650444,
   'lat_min': 51.45111771422115,
   'lon_max': 1.7629159916225028,
   'lon_min': -0.7457016982769984}},
 'EER_DEC_2013_GB_WGS84.7': {'EER13CD': 'E15000007',
  'EER13NM': 'London',
  'bbox': {'lat_max': 51.69184784058426,
   'lat_min': 51.286760163150866,
   'lon_max': 0.33399571714980253,
   'lon_min': -0.5102961470840263}},
 'EER_DEC_2013_GB_WGS84.8': {'EER13CD': 'E15000008',
  'EER13NM': 'South East',
  'bbox': {'lat_max': 52.1963232509333,
   'lat_min': 50.57492329367059,
   'lon_max': 1.4496584763156242,
   'lon_min': -1.9572320539920278}},
 'EER_DEC_2013_GB_WGS84.9': {'EER13CD': 'E15000009',
  'EER13NM': 'South West',
  'bbox': {'lat_max': 52.11257970443276,
   'lat_min': 49.864749468943316,
   'lon_max': -1.485726604041387,
   'lon_min': -6.418556174447501}}}

 