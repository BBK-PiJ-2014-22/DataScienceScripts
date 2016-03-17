# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 17:48:33 2016

Script to generate a set of 30 regions to use for WikiMapia purposes
Splits up 

@author: Jamie
"""

import areas

def getStats(bbox_list):    
    lats  = [i['lat_min'] for i in bbox_list]
    lats += [i['lat_max'] for i in bbox_list]
    lons  = [i['lon_min'] for i in bbox_list]
    lons += [i['lon_max'] for i in bbox_list]
    
    stats = {'lat_min':min(lats)
            ,'lon_min':min(lons)
            ,'lat_max':max(lats)
            ,'lon_max':max(lons)
            ,'lat_mid': (max(lats) + min(lats))/2
            ,'lon_mid': (min(lons) + max(lons))/2
            ,'lat_3rd':  max(lats) - (max(lats)-min(lats))*0.66}
    return stats

def printBBoxlist(tag, bboxlist):
    print("List:", tag)
    for i in bboxlist:
        print(i,":",bboxlist[i])
    print()

def splitBBox(bbox, x_divisions, y_divisions):
    '''Splits the bbox into a number of equal sized boxes
    
    X and Y determine how many times each axis is split to create the new set
    of boxes.
    
    A list of bboxes is returned.'''
    
    bbox_xlength = bbox['lon_max'] - bbox['lon_min']
    bbox_ylength = bbox['lat_max'] - bbox['lat_min']
    
    newbox_xl = bbox_xlength / x_divisions
    newbox_yl = bbox_ylength / y_divisions
    
    print('xlength:',bbox_xlength)   #TODO - remove debug
    print('ylength:',bbox_ylength)   #TODO - remove debug
    print('box x:'  ,newbox_xl)      #TODO - remove debug
    print('box y:'  ,newbox_yl)      #TODO - remove debug
    result = []
    
    for x in range(x_divisions):
        for y in range(y_divisions):
            newbox = {'lon_min': bbox['lon_min']+(x*newbox_xl)
                     ,'lon_max': bbox['lon_min']+((x+1)*newbox_xl)
                     ,'lat_min': bbox['lat_min']+(y*newbox_yl)
                     ,'lat_max': bbox['lat_min']+((y+1)*newbox_yl)
                     }
            if x == x_divisions-1:
                newbox['lon_max'] = bbox['lon_max']
            if y == y_divisions:
                newbox['lat_max'] = bbox['lat_max']

            result.append(newbox)
    return result

ladlist = areas.AREAS['lad']

all_bboxes = [i['bbox'] for i in ladlist]
all_stats  = getStats(all_bboxes)
bot_bboxes = [i for i in all_bboxes if i['lat_max'] < all_stats['lat_3rd']]
top_bboxes = [i for i in all_bboxes if i['lat_max'] >= all_stats['lat_3rd']]

bot_stats = getStats(bot_bboxes)
top_stats = getStats(top_bboxes)

newboxes = splitBBox(bot_stats,5,3)
print()
print(bot_stats)
print()
for i in newboxes:
    print(i)


