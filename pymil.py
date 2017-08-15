#!/usr/bin/python
# -*- coding: utf-8 -*-

#==============================================================================#
#      pymil - Open-source Carte internationale du Monde au Millionième        #
#                               Scale Codec                                    #
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

from __future__ import print_function

import re
from string import ascii_uppercase as zones
TWOM_30S = 0.125 / 3.0  # two minutes, thirty seconds


def dms_to_dd(dms):
    dms = dms.upper()
    signal = 1
    if dms[0] in "SW":
        signal = -1
        dms = dms[1:]
    parts = re.split("\D+", dms)
    dd = float(parts[0])
    if dd < 0:
        signal *= -1
        dd = abs(d)
    if len(parts) > 1:
        dd += float(parts[1])/60.
    if len(parts) > 2:
        dd += float(parts[2])/(60.*60.)
    return signal*dd


class CIM(object):
    def __init__(self, lat, lon, scale="25k"):
        """ Instantiates the CIM encoder, from latitude and longitude
        in either decimal degrees or degrees, minutes, seconds strings.
        sets __geo_interface__ to given scale, default 1:25.000."""
        try:
            lat = float(lat)
        except ValueError:
            lat = dms_to_dd(lat)
        try:
            lon = float(lon)
        except ValueError:
            lon = dms_to_dd(lon)

        self.scalesindex = {
            "500k": 0,
            "250k": 1,
            "100k": 2,
            "50k": 3,
            "25k": 4,
            "10k": 5,
            "1m": -1
        }
        self.coordinates = (
            lat, lon
        )
        la = abs(lat) % 4
        lo = abs(lon + 180) % 6
        self.scales = [
            (('V', 'X'), ('Y', 'Z'))[int(la % 4 / 2)][int(
                lo % 6 / 3)],  # 2 by 3                         1:500.000
            (('A', 'B'), ('C', 'D'))[int(la % 2 / 1)][int(
                lo % 3 /
                1.5)],  # 1 by 1.5                                    1:250.000
            (('I', 'II', 'III'), ('IV', 'V', 'VI'))[int(la % 1 / 0.5)][int(
                lo % 1.5 / 0.5)],  # 0.5 by 0.5               1:100.000
            (('1', '2'), ('3', '4'))[int(la % 0.5 / 0.25)][int(
                lo % 0.5 /
                0.25)],  # 0.25 by 0.25                        1:50.000
            (('NO', 'NE'), ('SO', 'SE'))[int(la % 0.25 / 0.125)][int(
                lo % 0.25 / 0.125)],  # 0.125 by 0.125             1:25.000
            (('A', 'B'), ('C', 'D'),
             ('E', 'F'))[int(la % 0.125 / TWOM_30S)][int(lo % 0.125 / 0.0625)]
        ]  #TWOM_30S by 0.0625 1:10.000
        self.hemisphere = "N" if lat > 0 else "S"  #(lat > 0) and "N" or "S"
        self.zone = zones[int(abs(lat)) // 4]
        self.fuse = str((180 + int(lon)) // 6 + 1)

        self.__geo_interface__ = self.get_geojson(scale)

    def __repr__(self):
        return "%s%s-%s-%s" % (self.hemisphere, self.zone, self.fuse,
                               "-".join(self.scales))

    def get_geojson(self, scale):
        """ Return a geoJSON representing the area and the code up to the scale requested. """
        w, e, n, s = bounding_coordinates(
            self.scales[0:self.scalesindex[scale] + 1], self.zone, self.fuse,
            self.hemisphere
        )
        return {
            "type": "Feature",
            "bbox" : (w, s, e, n),
            "properties": {"code": self.get_code(scale)},
            "geometry": {
                "type": "Polygon",
                "coordinates": (
                    (
                        (w, n),
                        (e, n),
                        (e, s),
                        (w, s),
                        (w, n)
                    ),
                )
            }
        }

    def get_code(self, scale):
        return (
            "%s%s-%s-%s" %
            (self.hemisphere, self.zone, self.fuse,
             "-".join(self.scales[0:self.scalesindex[scale] + 1]))
        ).strip("-")


def bounding_coordinates(scale_code, zone, fuse, hemisphere):
    """Return the bounding box for the given CIM encoded chart, in ((minlon, maxlon),(minlat, maxlat))"""
    coordinates = ({
        'V': (0.0, 0.0),
        'X': (0.0, 3.0),
        'Y': (2.0, 0.0),
        'Z': (2.0, 3.0)
    }, {
        'A': (0.0, 0.0),
        'B': (0.0, 1.5),
        'C': (1.0, 0.0),
        'D': (1.0, 1.5)
    }, {
        'I': (0.0, 0.0),
        'II': (0.0, 0.5),
        'III': (0.0, 1.0),
        'IV': (0.5, 0.0),
        'V': (0.5, 0.5),
        'VI': (0.5, 1.0)
    }, {
        '1': (0.0, 0.0),
        '2': (0.0, 0.25),
        '3': (0.25, 0.0),
        '4': (0.25, 0.25)
    }, {
        'NO': (0.0, 0.0),
        'NE': (0.0, 0.125),
        'SO': (0.125, 0.0),
        'SE': (0.125, 0.125)
    }, {
        'A': (0.0, 0.0),
        'B': (0.0, 0.0625),
        'C': (TWOM_30S, 0.0),
        'D': (TWOM_30S, 0.0625),
        'E': (TWOM_30S * 2, 0.0),
        'F': (TWOM_30S * 2, 0.0625)
    })
    dims = {
        0: (4.0, 6.0),
        1: (2.0, 3.0),
        2: (1.0, 1.5),
        3: (0.5, 0.5),
        4: (0.25, 0.25),
        5: (0.125, 0.125),
        6: (TWOM_30S, 0.0625)
    }[len(scale_code)]
    lat = zones.index(zone) * 4
    lat = lat if hemisphere == "N" else -lat
    lon = ((float(fuse) - 1) * 6 - 180)
    if scale_code:
        for scode, coords in zip(scale_code, coordinates):
            dy, dx = coords[scode]
            lon += dx
            lat -= dy
        return lon, lon + dims[1], lat, lat - dims[0]
    else:
        return lon, lon + 6.0, lat, lat - 4.0


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="""
            calculates CIM code for given coordinate pair,
            in either decimal degrees or degrees, minutes, seconds."""
    )
    parser.add_argument(
        "--geojson",
        action="store_true",
        dest="geojson",
        default=False,
        help="prints geoJSON of the map area instead of the code."
    )
    parser.add_argument(
        "--scale",
        action="store",
        dest="scale",
        default="25k",
        help="scale to be encoded, defaults to 1:25.000."
    )
    parser.add_argument(
        "latitude",
        action="store",
    )
    parser.add_argument(
        "longitude",
        action="store"
    )
    args = parser.parse_args()
    cimc = CIM(args.latitude, args.longitude, args.scale.lower())
    if args.geojson:
        import json
        print(json.dumps(cimc.__geo_interface__))
    else:
        print(cimc.get_code(args.scale))


if __name__ == "__main__":
    main()
