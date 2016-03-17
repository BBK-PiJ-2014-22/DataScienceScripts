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
import time

wmkey = 'E098D9EE-75F5D462-D06B8E5E-E7987CC9-5D1E23AC-FEF159D0-6DD91125-69BA7C7A'

result = []
wmareas = areas.AREAS['wikimapia2']
    
for i in range(len(wmareas)):
    if i > 1 and i % 30 == 0:
        print("Waiting for API IP address limit to reset...")
        time.sleep(10)
        
    print('Getting', wmareas[i]['wmboxid'], end=': ')
    try:
        found = wikimapia.getWMData(wmkey
                                   ,1362
                                   ,area = wmareas[i]['wmboxid']
                                   ,key_type ='wmboxid'
                                   ,level = 'wikimapia2')
        print('- Found:',len(found))
        result += found
    except (KeyError, TypeError):
        print(found)
        print(found.url)
        print(found.text)
        print('Error experienced for key',i,'for WM Box',wmareas[i]['wmboxid'])
        break
                               

result = [{'id'    : i['id']
          ,'title' : i['title'] 
          ,'bbox'  : wikimapia.getBBox(i['polygon'],'x','y')}
        for i in result
        ]
for i in result:
    i['x'] = numpy.mean((i['bbox']['lon_min'], i['bbox']['lon_max']))
    i['y'] = numpy.mean((i['bbox']['lat_min'], i['bbox']['lat_max']))
        
with open('london_mosques.csv', 'a') as csvfile:
    fieldnames = ('id','title','x','y','bbox')
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames, lineterminator='\n')
    writer.writeheader()
    for i in result:
        try:
            writer.writerow(i)
        except UnicodeEncodeError:
            i['title'] = 'Unreadable Name'
            writer.writerow(i)
        
        
csvfile.close()
