#!/usr/bin/env python3

import sys
import binwalk
import os
import shutil
import numpy
import tifffile

colorimguuid = "c65a358c-2782-481d-9f05-b9b233b3802d"
heightimguuid = "4cdb0c75-5706-48cc-a9a1-adf395d609ae"

binwalkpath="_"+sys.argv[1]+".extracted/"

if(os.path.exists(binwalkpath)):
    shutil.rmtree(binwalkpath)

binwalk.scan(sys.argv[1],signature=True,quiet=True,extract=True)

colorimgpath= binwalkpath+colorimguuid
if(os.path.exists(colorimgpath)):
    size = os.path.getsize(colorimgpath)
    colorimgraw = open(colorimgpath,'rb')
    colorimgout = open(sys.argv[1]+".color.bmp",'wb')
    colorimgout.write(b"BM"+(size+138-16).to_bytes(4, byteorder='little')+b"\x00\x00\x00\x00\x8a\x00\x00\x00\x7c\x00")
    colorimgout.write(b"\x00\x00"+colorimgraw.read(8)+b"\x01\x00\x18\x00\x00\x00")
    colorimgout.write(b"\x00\x00\x00\x00\x24\x00\x23\x2e\x00\x00\x23\x2e\x00\x00\x00\x00")
    colorimgout.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\xff\x00\x00\xff\x00")
    colorimgout.write(b"\x00\x00\x00\x00\x00\x00\x42\x47\x52\x73\x00\x00\x00\x00\x00\x00")
    colorimgout.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    colorimgout.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    colorimgout.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00")
    colorimgout.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    colorimgraw.seek(16,0)
    colorimgout.write(colorimgraw.read())
    colorimgraw.close()
    colorimgout.close()


heightimgpath= binwalkpath+heightimguuid
if(os.path.exists(heightimgpath)):
    heightimgnp = numpy.fromfile(heightimgpath,numpy.int32)
    xsize=heightimgnp[0]
    ysize=heightimgnp[1]
    heightimgnp=numpy.delete(heightimgnp, [0,1,2,3],None)
    print(heightimgnp[0:100])
    print(ysize,xsize)
    heightimgnp=heightimgnp.reshape(ysize,xsize)
    tifffile.imwrite(sys.argv[1]+".height.tif", heightimgnp)
    
shutil.rmtree(binwalkpath)
