#!/usr/bin/env python

import time
import os
import sys
import cv2
import caffe
import numpy as np


if (len(sys.argv) != 2):
	print "object_detection_single: <imagefn>"
	quit()

imagefn=sys.argv[1]

DISPLAY_RESULT=False

# Configure Caffe to use the GPU for inference
caffe.set_mode_gpu()

MODEL_DIR="data/"
last_iteration='37300'


b = caffe.proto.caffe_pb2.BlobProto()
data = open(MODEL_DIR+'mean.binaryproto','rb').read()
b.ParseFromString(data)
mean = np.array(caffe.io.blobproto_to_array(b))[0]

mean=np.swapaxes(mean,0,2)
mean=np.swapaxes(mean,0,1)


# Instantiate a Caffe model in GPU memory
# The model architecture is defined in the deploy.prototxt file
# The pretrained model weights are contained in the snapshot_iter_<number>.caffemodel file
os.environ['GLOG_minloglevel']='3'
classifier = caffe.Net(os.path.join(MODEL_DIR,'deploy.prototxt'), 
                       os.path.join(MODEL_DIR,'snapshot_iter_' + last_iteration + '.caffemodel'),
                       caffe.TEST)

# Instantiate a Caffe Transformer object that wil preprocess test images before inference
transformer = caffe.io.Transformer({'data': classifier.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))
#transformer.set_mean('data',mean.mean(1).mean(1)/255)
transformer.set_raw_scale('data', 255)
transformer.set_channel_swap('data', (2,1,0))
BATCH_SIZE, CHANNELS, HEIGHT, WIDTH = classifier.blobs['data'].data[...].shape

print 'The input size for the network is: (' + \
        str(BATCH_SIZE), str(CHANNELS), str(HEIGHT), str(WIDTH) + \
         ') (batch size, channels, height, width)'

print imagefn
frame=cv2.imread(imagefn)
if frame is None:
	print "error, could not read code"
	quit()

image_height=frame.shape[0]
image_width=frame.shape[1]

od_frame=cv2.resize(frame,(WIDTH,HEIGHT),0,0)
    
t1 = time.time()

data = transformer.preprocess('data', od_frame.astype('float16')/255)
# Set the preprocessed frame to be the Caffe model's data layer
classifier.blobs['data'].data[...] = data
# Measure inference time for the feed-forward operation
# The output of DetectNet is an array of bounding box predictions
bounding_boxes = classifier.forward()['bbox-list'][0]

box_found=False
for bbox in bounding_boxes:
	if bbox.sum() > 0:
		box_found=True

		#scale image back to input
		b0=np.int(bbox[0]/WIDTH*image_width)
		b1=np.int(bbox[1]/HEIGHT*image_height)
		b2=np.int(bbox[2]/WIDTH*image_width)
		b3=np.int(bbox[3]/HEIGHT*image_height)
		w=b2-b0
		h=b3-b1
		print "Bounding box: X=%d Y=%d W=%d H=%d" % (b0,b1,w,h)

		cv2.rectangle(frame, (b0,b1), (b2,b3), (255, 0, 0), -1)


if not box_found:
	print "No bounding boxes found"

if DISPLAY_RESULT:
	cv2.imshow('image',frame)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


