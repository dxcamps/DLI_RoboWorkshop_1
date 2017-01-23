
import sys
import os
import re
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


if len(sys.argv) != 3:
    print "invert_images <input_dir> <output_odir>"
    quit()


idir=sys.argv[1]
odir=sys.argv[2]

mkdir_if_needed(odir)
for i in range(0,10):
    mkdir_if_needed("%s/%d" % (odir,i))

cnt=0
for dir,subdir,fnlist in os.walk(idir):
    for fn in fnlist:
	ffn="%s/%s" % (dir,fn)
	ofn="%s/invert_%s" % (dir,fn)
        ofn=re.sub(r'^'+idir,odir,ofn)
        lnfn=re.sub(r'^'+idir,odir,ffn)

	img=scipy.misc.imread(ffn)
	# Now 
	# Now invert the image
	n_img=255-img
	# Now write the image
 	scipy.misc.imsave(ofn,n_img)
	if (cnt%2000) == 0:
            print "Converted %d files" % (cnt)
        cnt=cnt+1

	# Link the original into this directory
        print "../../"+ffn,lnfn 
        os.symlink("../../"+ffn,lnfn)


#    label=ord(lar[loffset+i])
#    ofn="%s/%d/img_%d.png" % (odir,label,i)
#    b=np.fromstring(dar[doffset+i*dsz:],dtype=np.uint8,count=dsz)
#    img=np.reshape(b,(28,28))
#    scipy.misc.imsave(ofn,img)
#    if (i%2000) == 0:
#       print "Processed %d of %d images" % (i,dcnt)

