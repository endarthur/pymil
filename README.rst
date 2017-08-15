=====================================================================================
pymil - Open-source Carte internationale du Monde au Millionième nomenclature encoder
=====================================================================================

Pymil is a simple Carte internationale du Monde au Millionième nomenclature coder. You
might find it useful for searching maps for a specific coordinate pair.

```
usage: pymil.py [-h] [--geojson] [--scale SCALE] latitude longitude

calculates CIM code for given coordinate pair.

positional arguments:
  latitude
  longitude

optional arguments:
  -h, --help     show this help message and exit
  --geojson      prints geoJSON of the map area instead of the code.
  --scale SCALE  scale to be encoded, defaults to 1:25.000.
```

CIM
===

The CIM uses the geographic coordinate system as background for the Earth separation,
each individual chart receives a code that is composed by two letters and a number.
The two letters represent respectively the hemisphere (north or south) and a interval
of 4° in Earth's latitude, which follow the alphabetical order starting from the Equator
and increasing to the poles. The number represents a interval of 6° in longitude,
marked with numbers and starting in the 180° meridian.

The letters that follow this are subdivisions of the basic millionth chart and
indicates charts in scales 1 to 500,000, 250,000, 100,000, 50,000 and 25,000.
The letter/number used in each part of the code deppends on the relative position
of the chart to its smaller scale counterpar.
    
TODO
====

* Make better docs.

__geo_interface__
=================

The class CIM includes a __geo_interface__, as defined in https://gist.github.com/sgillies/2217756

Thanks
======

* Luis Urtiga for the CIM nomenclature explanation.


