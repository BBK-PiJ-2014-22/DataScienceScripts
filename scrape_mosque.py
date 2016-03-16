# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 16:33:53 2016

Quick hacky script to extract mosque information

@author: Jamie
"""

import wikimapia
import csv
import numpy
import areas

wmkey = 'E098D9EE-75F5D462-D06B8E5E-E7987CC9-5D1E23AC-FEF159D0-6DD91125-69BA7C7A'

result = []
lads = areas.AREAS['lad']

for i in range(len(lads)):
    print('Getting', lads[i]['name'], end=': ')
    try:
        found = wikimapia.getWMData(wmkey
                                   ,1362
                                   ,area = lads[i]['LAD12CD']
                                   ,key_type ='LAD12CD'
                                   ,level = 'lad')
        print('- Found:',len(found))
        result += found
    except KeyError:
        print('API limit reached at key',i,'for LAD',lads[i]['name'])
        break
                               

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
        try:
            writer.writerow(i)
        except UnicodeEncodeError:
            i['title'] = 'Unreadable Name'
            writer.writerow(i)
        
        
csvfile.close()
