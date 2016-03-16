# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 16:33:53 2016

Quick hacky script to extract mosque information

@author: Jamie
"""

import wikimapia
import csv
import numpy

wmkey = 'E098D9EE-75F5D462-D06B8E5E-E7987CC9-5D1E23AC-FEF159D0-6DD91125-69BA7C7A'

result = wikimapia.getWMData(wmkey,1362)
result = [{'id'    : i['id']
          ,'title' : i['title'] 
          ,'bbox'  : wikimapia.getBBox(i['polygon'],'x','y')}
        for i in result
        ]
for i in result:
    i['x'] = numpy.mean((i['bbox']['lon_min'], i['bbox']['lon_max']))
    i['y'] = numpy.mean((i['bbox']['lat_min'], i['bbox']['lat_max']))
        
with open('london_mosques.csv', 'w') as csvfile:
    fieldnames = ['id', 'title','x','y','bbox']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames, lineterminator='\n')
    writer.writeheader()
    for i in result:
        writer.writerow(i)
        
csvfile.close()
