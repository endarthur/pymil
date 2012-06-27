from string import uppercase as zone
from decimaldegrees import dms2decimal as precon
from scale import find_scale
#Find the IMC code of the chart that include the point given.


def find_fuse(lon):
	return str((180 + int(lon))/6 + 2)

def find_zone(lat):
    return zone[int(abs(lat))/4]
    
def encode_IMC(lat, lon):
    if lat > 0:
        hemisphere = 'N'
    else:
        hemisphere = 'S'
    return hemisphere + find_zone(lat) + find_fuse(lon) + '-' + find_scale(lat, lon)

 
if __name__ == '__main__':
    #~ lat, lon = precon(68, 45, 13), precon(113, 21, 11)
    lon, lat = (-61,-11)
    print int(abs(lat))/4
    print encode_IMC(lat, lon)
