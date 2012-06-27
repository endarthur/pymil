import math
import string
import decimaldegrees as dd

precon = dd.dms2decimal

def longitude(l):
	return (180 + int(l))/6 + 1

def latitude(l):
    return string.lowercase[int(l)/4]

def onetofivehund(lat, lon):
    d = [['v', 'x'], ['y', 'z']]
    return d[(int(lat)%6)/2][(int(lon)%4)/2]
    
if __name__ == '__main__':
    lat, lon = precon(68, 45, 13), precon(113, 21, 11)
    print lat, lon
