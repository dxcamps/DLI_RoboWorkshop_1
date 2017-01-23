
import sys
import os
import scipy as sc
import scipy.misc
import numpy as np

def stoi(a):
   return ((ord(a[0])*256+ord(a[1]))*256+ord(a[2]))*256+ord(a[3])

def mkdir_if_needed(d):
    try:
        os.stat(d)
    except:
        print "Creating directory: %s" % (d)
        os.mkdir(d)


if len(sys.argv) != 4:
    print "convert_mnist_to_png <datafile> <labelfile> <odir>"
    quit()


dfn=sys.argv[1]
lfn=sys.argv[2]
odir=sys.argv[3]

dar=open(dfn,"rb").read()

dmagic=stoi(dar[0:4])
dcnt=stoi(dar[4:8])
nrows=stoi(dar[8:12])
ncols=stoi(dar[12:16])

lar=open(lfn,"rb").read()
lmagic=stoi(dar[0:4])
lcnt=stoi(dar[4:8])

if lcnt != dcnt: 
    print "Error: records counts do not match (%d vs. %d)" % (lcnt,dcnt)
    quit()

# Create directories 0 through 9 as needed
mkdir_if_needed(odir)
for l in range(0,10):
    d="%s/%d" % (odir,l)
    mkdir_if_needed(d)

doffset=16
loffset=8
dsz=nrows*ncols
for i in range(0,dcnt):
    label=ord(lar[loffset+i])
    ofn="%s/%d/img_%d.png" % (odir,label,i)
    b=np.fromstring(dar[doffset+i*dsz:],dtype=np.uint8,count=dsz)
    img=np.reshape(b,(28,28))
    scipy.misc.imsave(ofn,img)
    if (i%2000) == 0:
       print "Processed %d of %d images" % (i,dcnt)

