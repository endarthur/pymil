#!/usr/bin/python
# -*- coding: utf-8 -*-
# Somewhat hackish way to process all MSed areas... Gosh, this sounds like Perl...
import csv
from collections import defaultdict
#~ from datetime import date

#~ from decconv import mag_declination, grid_convergence

from pymil import code

with open("areasMS.csv") as f:
    points = list(csv.reader(f))[1:]
    
codes_by_area = defaultdict(set)
    
for lon, lat, point in points:
    print point, lat, lon
    lat = float(lat)
    lon = float(lon)
    cim = code(lat, lon)
    print cim
    codes_by_area[int(point)].add(repr(cim))
    #~ dec = mag_declination(lat, lon, date(2012, 1, 1))
    #~ convr = grid_convergence(lat, lon)
    #~ stuff.append([point, lon, lat, dec[0], dec[1], convr])
    
stuff = []
    
for code in codes_by_area.keys():
    foo = [code] + list(codes_by_area[code])
    stuff.append(foo)

print codes_by_area.keys()

print stuff

with open("outcodes.csv", "w") as f:
    outp = csv.writer(f)
    outp.writerow(["id", "code", "code", "code", "code"])
    outp.writerows(stuff)
