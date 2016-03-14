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
result = {i : {'title' : result[i]['title'] 
            ,'bbox' : wikimapia.getBBox(result[i]['polygon'],'x','y')}
        for i in result
        }
for i in result:
    result[i]['x'] = numpy.mean((result[i]['bbox']['lon_min'], result[i]['bbox']['lon_max']))
    result[i]['y'] = numpy.mean((result[i]['bbox']['lat_min'], result[i]['bbox']['lat_max']))
        
with open('london_mosques.csv', 'w') as csvfile:
    fieldnames = ['id', 'title','x','y','bbox']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames, lineterminator='\n')
    writer.writeheader()
    for i in result:
        row = {'id':i}
        row.update(result[i])
        writer.writerow(row)
        
csvfile.close()
