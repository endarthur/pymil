# A International World Map encoder - from geographic coordinates
# May someday accept UTM as well, but tonight it will be simpler
# OO mode, hopefully

from string import uppercase as zone


def find_scale(lat, lon):
    five_hundred = (('V', 'X'), ('Y', 'Z')) # 2 by 3
    two_hundred_fifty = (('A', 'B'), ('C', 'D')) # 1 by 1.5
    one_hundred = (('I', 'II', 'III'), ('IV', 'V', 'VI')) # 0.5 by 0.5
    fifty = (('1', '2'), ('3', '4')) # 0.25 by 0.25
    twenty_five = (('NO', 'NE'), ('SO', 'SE')) # 0.125 by 0.125
    scale = five_hundred[int(lat % 4 / 2)][int(lon % 6 / 3)]
    scale += '-' + two_hundred_fifty[int(lat % 2 / 1)][int(lon % 3 / 1.5)]
    scale += '-' + one_hundred[int(lat % 1 / 0.5)][int(lon % 1.5 / 0.5)]
    scale += '-' + fifty[int(lat % 0.5 / 0.25)][int(lon % 0.5 / 0.25)]
    scale += '-' + twenty_five[int(lat % 0.25 / 0.125)][int( lon % 0.25 / 0.125)]
    return scale

class CIMcode(object):
    def __init__(self, lat, lon):
        """ Create the CIMcode object, from latitude and longitude in decimal degrees. """
        self.coordinates = (lat, lon)
        self.scales = {"500k":(('V', 'X'), ('Y', 'Z'))[int(lat % 4 / 2)][int(lon % 6 / 3)], # 2 by 3
"250k":(('A', 'B'), ('C', 'D'))[int(lat % 2 / 1)][int(lon % 3 / 1.5)], # 1 by 1.5
"100k":(('I', 'II', 'III'), ('IV', 'V', 'VI'))[int(lat % 1 / 0.5)][int(lon % 1.5 / 0.5)], # 0.5 by 0.5
"50k":(('1', '2'), ('3', '4'))[int(lat % 0.5 / 0.25)][int(lon % 0.5 / 0.25)], # 0.25 by 0.25
"25k":(('NO', 'NE'), ('SO', 'SE'))[int(lat % 0.25 / 0.125)][int( lon % 0.25 / 0.125)]} # 0.125 by 0.125
        self.hemisphere = (lat > 0) and "N" or "S"
        self.zone = zone[int(abs(lat))/4]
        self.fuse = str((180 + int(lon))/6 + 2)
        #~ scale = five_hundred[int(lat % 4 / 2)][int(lon % 6 / 3)]
        #~ scale += '-' + two_hundred_fifty[int(lat % 2 / 1)][int(lon % 3 / 1.5)]
        #~ scale += '-' + one_hundred[int(lat % 1 / 0.5)][int(lon % 1.5 / 0.5)]
        #~ scale += '-' + fifty[int(lat % 0.5 / 0.25)][int(lon % 0.5 / 0.25)]
        #~ scale += '-' + twenty_five[int(lat % 0.25 / 0.125)][int( lon % 0.25 / 0.125)]
    def __repr__(self):
        return "%s%s-%s-%s" % (self.hemisphere, self.zone, self.fuse, "-".join(self.scales))
            
            
