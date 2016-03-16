# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 15:00:48 2016

Script to convert a shapefile to usable json format and saves it as a text file

This is a static script to create the data once rather than on the fly. 

@author: Jamie
"""

import shapefile
import json
from osgbconverter import OSGB36toWGS84 as osc

path = 'C:\Programming\data\LADBoundaries\data\LAD_DEC_2012_GB_BFE'
sr = shapefile.Reader(path)
data = sr.shapeRecords()

lad = [{'LAD12CD'   : i.record[0]
       ,'name'      : i.record[2]
       ,'bbox'      : {'lat_min': osc(i.shape.bbox[0], i.shape.bbox[1])[0]
                      ,'lon_min': osc(i.shape.bbox[0], i.shape.bbox[1])[1]
                      ,'lat_max': osc(i.shape.bbox[2], i.shape.bbox[3])[0]
                      ,'lon_max': osc(i.shape.bbox[2], i.shape.bbox[3])[1]}
       ,'oldbbox'   : tuple(i.shape.bbox)}
       for i in data]

with open('counties.txt', 'w') as output:
    json.dump(lad, output, sort_keys = True, indent = 2)

