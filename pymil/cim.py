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
from string import uppercase as zone

class code(object):
    def __init__(self, lat, lon):
        """ Create the pymil object, from latitude and longitude in decimal degrees. 
        In the future, hopefully, it will be possible to use different syntaxes for lat and lon."""
        self.scalesindex = {"500k": 0, "250k": 1, "100k": 2, "50k": 3, "25k": 4}
        self.coordinates = (lat, lon) # Just might be useful to store a small coordinates tupple. Who knows?
        self.scales = [(('V', 'X'), ('Y', 'Z'))[int(lat % 4 / 2)][int(lon % 6 / 3)], # 2 by 3
        (('A', 'B'), ('C', 'D'))[int(lat % 2 / 1)][int(lon % 3 / 1.5)], # 1 by 1.5
        (('I', 'II', 'III'), ('IV', 'V', 'VI'))[int(lat % 1 / 0.5)][int(lon % 1.5 / 0.5)], # 0.5 by 0.5
        (('1', '2'), ('3', '4'))[int(lat % 0.5 / 0.25)][int(lon % 0.5 / 0.25)], # 0.25 by 0.25
        (('NO', 'NE'), ('SO', 'SE'))[int(lat % 0.25 / 0.125)][int( lon % 0.25 / 0.125)]] # 0.125 by 0.125
        self.hemisphere = (lat > 0) and "N" or "S"
        self.zone = zone[int(abs(lat))/4]
        self.fuse = str((180 + int(lon))/6 + 2)
    def __repr__(self):
        """ Just cat everything in the max scale defined by the CIM code. """
        return "%s%s-%s-%s" % (self.hemisphere, self.zone, self.fuse, "-".join(self.scales))
    def __getitem__(self, scale):
        """ Return a list with the scale codes up to the scale requested. """
        return self.scales[0:self.scalesindex[scale] + 1]
