=====================================================================================
pymil - Open-source Carte internationale du Monde au Millionième nomenclature encoder
=====================================================================================

Pymil is a simple Carte internationale du Monde au Millionième nomenclature coder. You
might find it useful for searching maps for a specific coordinate pair. Typical usage
would be something like::

    #!/usr/bin/env python
    
    import pymil
    
    map = pymil.code(-11, -61) #Currently uses only decimal degrees;
    map["100k"] #Returns a list containing the code elements for the 1:100k map that contains the area.
    print map #Returns the code for 1:25k by default, in a string
    
TODO
====

* Make better docs. Explain what the hell the CIM code is, with images.
* Extend functionality, maybe letting you use UTM and whatsoever.




