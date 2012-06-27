# A International World Map encoder - from geographic coordinates
# May someday accept UTM as well, but tonight it will be simpler

def find_scale(lat, lon):
    five_hundred = [['V', 'X'], ['Y', 'Z']] # 2 by 3
    two_hundred_fifty = [['A', 'B'], ['C', 'D']] # 1 by 1.5
    one_hundred = [['I', 'II', 'III'], ['IV', 'V', 'VI']] # 0.5 by 0.5
    fifty = [['1', '2'], ['3', '4']] # 0.25 by 0.25
    twenty_five = [['NO', 'NE'], ['SO', 'SE']] # 0.125 by 0.125
    scale = five_hundred[int(lat % 4 / 2)][int(lon % 6 / 3)]
    scale += '-' + two_hundred_fifty[int(lat % 2 / 1)][int(lon % 3 / 1.5)]
    scale += '-' + one_hundred[int(lat % 1 / 0.5)][int(lon % 1.5 / 0.5)]
    scale += '-' + fifty[int(lat % 0.5 / 0.25)][int(lon % 0.5 / 0.25)]
    scale += '-' + twenty_five[int(lat % 0.25 / 0.125)][int( lon % 0.25 / 0.125)]
    return scale

if __name__ == '__main__':
    print find_scale(68.7536111, 113.3530555)
    print find_scale(-61, -11)
    
        
