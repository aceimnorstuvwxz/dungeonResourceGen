#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
(C) 2015 ScatOrc
'''

import sys
from pylab import*
from scipy.io import wavfile
from PIL import Image, ImageDraw
import json
import random
import time

ImageWidth = 1024
ImageHeight = 1024

NUM_UNIT = 8
WIDTH_UNIT = 128

'''
texture的逻辑的原点在左下方。
实际绘制时，对Y方向要进行处理。

'''


def flipY(xy):
    ret = []
    for t in xy:
        ret.append((t[0], ImageHeight - 1 - t[1]))
    return ret

def generatePerFrame(frameData, draw):
    frameIndex = frameData["frameIndex"]
    baseCenterX = frameIndex%NUM_UNIT * WIDTH_UNIT + WIDTH_UNIT/2
    baseCenterY = int(frameIndex/NUM_UNIT) * WIDTH_UNIT * 2 + WIDTH_UNIT/2
    
    pointsMap = {}
    for point in frameData["points"]:
        pointsMap[point["pid"]] = point
    
    for triangle in frameData["triangles"]:
        baseColor = (int(255*triangle["cr"]),int(255*triangle["cg"]),int(255*triangle["cb"]),int(255*triangle["ca"]))
        pa = pointsMap[triangle["pa"]]
        pb = pointsMap[triangle["pb"]]
        pc = pointsMap[triangle["pc"]]
        ''' draw base color '''
        baseA = (baseCenterX + pa["x"]*0.5*WIDTH_UNIT, baseCenterY + pa["y"]*0.5*WIDTH_UNIT)
        baseB = (baseCenterX + pb["x"]*0.5*WIDTH_UNIT, baseCenterY + pb["y"]*0.5*WIDTH_UNIT)
        baseC = (baseCenterX + pc["x"]*0.5*WIDTH_UNIT, baseCenterY + pc["y"]*0.5*WIDTH_UNIT)

        draw.polygon(flipY([baseA, baseB, baseC]), fill=baseColor)
    

def generateTexture(data, fn):
    img = Image.new("RGBA", (ImageWidth,ImageHeight), color=(0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    for frame in data['frames']:
        print frame
        generatePerFrame(frame, draw)
        
    img.save(fn, 'PNG')
  


if __name__ == "__main__":
    fn = "example.json"
    fn_out = "example_out.png"
    f = open(fn, "r")
    jsondata = f.readline()
    data = json.loads(jsondata)
    print data
    generateTexture(data, fn_out)
    
    print 'DONE'
