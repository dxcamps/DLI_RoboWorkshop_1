#!/bin/bash

BDIR=$(cd $(dirname $0) && pwd)

# Get data
rm *ubyte
wget http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz
wget http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz
wget http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz
wget http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz

gunzip *.gz

# Create the full dataset from downloaded files as [train,test]_full

for d in train_full test_full; do
	if [ ! -d $d ]; then
		mkdir $d
	fi
done
python $BDIR/convert_mnist_to_png.py train-images-idx3-ubyte train-labels-idx1-ubyte train_full
python $BDIR/convert_mnist_to_png.py t10k-images-idx3-ubyte t10k-labels-idx1-ubyte test_full

# Create the 10% dataset into [train,test]_small

for d in train_full test_full; do
	find $d -type d | sed 's/_full/_small/' | xargs -n 1 mkdir
	find $d/ -type f | shuf | head -6000 | xargs -I '{}' echo {} {} | sed 's/_full/_small/2' | xargs -n 2 cp
done



# Create the inverted data set as [train,test]_invert
python $BDIR/invert_images.py train_full train_invert
python $BDIR/invert_images.py test_full test_invert


