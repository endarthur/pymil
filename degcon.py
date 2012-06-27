def decdeg2dms(dd):
    mnt, sec = divmod(dd*3600,60)
    deg, mnt = divmod(mnt,60)
    return deg, mnt, sec
