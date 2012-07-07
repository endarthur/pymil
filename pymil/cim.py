#!/usr/bin/python
# -*- coding: utf-8 -*-

#==============================================================================#
#      pymil - Open-source Carte internationale du Monde au Millionième        #
#                               Scale Coder                                    #
#                                                                              #
#    Copyright (c)  2012 Arthur Endlein.                                       #
#                                                                              #
#                                                                              #
#    This file is part of pymil.                                               #
#                                                                              #
#    pymil is free software: you can redistribute it and/or modify             #
#    it under the terms of the GNU General Public License as published by      #
#    the Free Software Foundation, either version 3 of the License, or         #
#    (at your option) any later version.                                       #
#                                                                              #
#    pymil is distributed in the hope that it will be useful,                  #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#    GNU General Public License for more details.                              #
#                                                                              #
#    You should have received a copy of the GNU General Public License         #
#    along with pymil.  If not, see <http://www.gnu.org/licenses/>.            #
#                                                                              #
#                                                                              #
#==============================================================================#

# A International World Map encoder - from geographic coordinates
# May someday accept UTM as well, but tonight it will be simpler
# OO mode, hopefully. Maybe.
# Eventually decoder, as well. Yep, it decodes. Horribly hackish, though. Must better that.
from string import uppercase as zones

class code(object):
    def __init__(self, lat, lon):
        """ Create the pymil object, from latitude and longitude in decimal degrees. 
        In the future, hopefully, it will be possible to use different syntaxes for lat and lon."""
        self.scalesindex = {"500k": 0, "250k": 1, "100k": 2, "50k": 3, "25k": 4}
        self.coordinates = (lat, lon) # Just might be useful to store a small coordinates tupple. Who knows?
        print self.coordinates
        la = abs(lat) % 4
        lo = abs(lon + 180) % 6
        print la, lo
        self.scales = [(('V', 'X'), ('Y', 'Z'))[int(la % 4 / 2)][int(lo % 6 / 3)], # 2 by 3               1:500.000
        (('A', 'B'), ('C', 'D'))[int(la % 2 / 1)][int(lo % 3 / 1.5)], # 1 by 1.5                          1:250.000
        (('I', 'II', 'III'), ('IV', 'V', 'VI'))[int(la % 1 / 0.5)][int(lo % 1.5 / 0.5)], # 0.5 by 0.5     1:100.000
        (('1', '2'), ('3', '4'))[int(la % 0.5 / 0.25)][int(lo % 0.5 / 0.25)], # 0.25 by 0.25              1:50.000
        (('NO', 'NE'), ('SO', 'SE'))[int(la % 0.25 / 0.125)][int( lo % 0.25 / 0.125)]] # 0.125 by 0.125   1:25.000
        self.hemisphere = (lat > 0) and "N" or "S"
        self.zone = zones[int(abs(lat))/4]
        self.fuse = str((180 + int(lon))/6 + 1)
    def __repr__(self):
        """ Just cat everything in the max scale defined by the CIM code. """
        return "%s%s-%s-%s" % (self.hemisphere, self.zone, self.fuse, "-".join(self.scales))
    def __getitem__(self, scale):
        """ Return a tuple with the bounding latitude and longitude and a list with the scale codes up to the scale requested. """
        #~ return [self.hemisphere, self.zone, self.fuse] + self.scales[0:self.scalesindex[scale] + 1]
        return bounding_coordinates(self.scales[0:self.scalesindex[scale] + 1], self.zone, self.fuse, self.hemisphere), "%s%s-%s-%s" % (self.hemisphere, self.zone, self.fuse, "-".join(self.scales[0:self.scalesindex[scale] + 1]))#[self.hemisphere, self.zone, self.fuse] + self.scales[0:self.scalesindex[scale] + 1]

def bounding_coordinates( scale_code, zone, fuse, hemisphere):
    """Return the bounding box for the given CIM encoded chart, in ((minlon, maxlon),(minlat, maxlat))"""
    coordinates = ({'V':(0.0, 0.0), 'X':(0.0, 3.0), 'Y':(2.0, 0.0), 'Z':(2.0, 3.0)},
    {'A':(0.0, 0.0), 'B':(0.0, 1.5), 'C':(1.0, 0.0), 'D':(1.0, 1.5)},
    {'I':(0.0, 0.0), 'II':(0.0, 0.5), 'III':(0.0, 1.0), 'IV':(0.5, 0.0), 'V':(0.5, 0.5), 'VI':(0.5, 1.0)},
    {'1':(0.0, 0.0), '2':(0.0, 0.25), '3':(0.25, 0.0), '4':(0.25, 0.25)},
    {'NO':(0.0, 0.0), 'NE':(0.0, 0.125), 'SO':(0.125, 0.0), 'SE':(0.125, 0.125)})
    dims = {1:(2.0, 3.0), 2:(1.0, 1.5), 3:(0.5, 0.5), 4:(0.25, 0.25), 5:(0.125, 0.125)}[len(scale_code)]
    print dims
    lat = zones.index(zone) * 4
    print lat
    lat = hemisphere == "N" and lat or -lat
    print lat
    lon = ((float(fuse) - 1)*6 - 180)
    print "fuse", fuse
    print "longitude", lon
    if scale_code:
        for scode, coords in zip(scale_code, coordinates):
            dy, dx = coords[scode]
            print "dlon, dlat\t", dx, dy
            lon += dx
            lat -= dy
            print "lon, lat\t", lon, lat
        #~ lon -= 180
        return lon, lon + dims[1], lat, lat - dims[0] #, lon), (lat - dims[0], lon + dims[1]))
    else:
        #~ lon -= 180
        return lon, lon + 6.0, lat, lat - 4.0
        
        
    
if __name__ == "__main__":
    cimc = code(-11.4, -54.4)
    print cimc
    print cimc["50k"]
    cimc = code(-22.5, -47.7)
    print cimc
    print cimc["50k"]
    
