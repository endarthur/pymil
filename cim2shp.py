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

import os, os.path, shutil
import osgeo.ogr
import osgeo.osr


def make_shape(minLon, maxLon, minLat, maxLat, cimCode):
    
    if os.path.exists("bounding-box"):
        shutil.rmtree("bounding-box")
    os.mkdir("bounding-box")
    dstPath = os.path.join("bounding-box", "boundingBox.shp")

    
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS('WGS84')
    #~ We can now create the Shapefile itself using this spatial reference:
    driver = osgeo.ogr.GetDriverByName("ESRI Shapefile")
    dstFile = driver.CreateDataSource(dstPath)
    dstLayer = dstFile.CreateLayer("layer", spatialReference)
    
    #~ 2.	 After creating the Shapefile, you next define the various fields that will hold
    #~ the metadata for each feature. In this case, let's add two fields to store the
    #~ country name and its ISO-3166 code:
    #~ fieldDef = osgeo.ogr.FieldDefn("COUNTRY", osgeo.ogr.OFTString)
    #~ fieldDef.SetWidth(50)
    #~ dstLayer.CreateField(fieldDef)
    
    fieldDef = osgeo.ogr.FieldDefn("CIMCODE", osgeo.ogr.OFTString)
    fieldDef.SetWidth(20)
    dstLayer.CreateField(fieldDef)
    
    #~ 3.	 We now need to create the geometry for each feature—in this case, a polygon
    #~ defining the country's bounding box. A polygon consists of one or more
    #~ linear rings; the first linear ring defines the exterior of the polygon, while
    #~ additional rings define "holes" inside the polygon. In this case, we want a
    #~ simple polygon with a square exterior and no holes:
    
    linearRing = osgeo.ogr.Geometry(osgeo.ogr.wkbLinearRing)
    linearRing.AddPoint(minLon, minLat)
    linearRing.AddPoint(maxLon, minLat)
    linearRing.AddPoint(maxLon, maxLat)
    linearRing.AddPoint(minLon, maxLat)
    linearRing.AddPoint(minLon, minLat)
    polygon = osgeo.ogr.Geometry(osgeo.ogr.wkbPolygon)
    polygon.AddGeometry(linearRing)
    print minLon, maxLon, minLat, maxLat
    #~ Once we have the polygon, we can use it to create a feature:
    
    feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
    feature.SetGeometry(polygon)
    feature.SetField("CIMCODE", cimCode)
    dstLayer.CreateFeature(feature)
    feature.Destroy()
    
    #~ Notice how we use the setField() method to store the feature's
    #~ metadata. We also have to call the Destroy() method to close the
    #~ feature once we have finished with it; this ensures that the feature is
    #~ saved into the Shapefile.
    #~ 4.	 Finally, we call the Destroy() method to close the output Shapefile:
    
    dstFile.Destroy()
    
if __name__=="__main__":
    from pymil import code
    ccode = code(-22.5, -47.7)
    coords, cimCode = ccode["50k"]
    print cimCode
    #~ cimCode = repr(ccode)
    #~ minLon, maxLon, minLat, maxLat
    make_shape(*coords, cimCode=cimCode)
