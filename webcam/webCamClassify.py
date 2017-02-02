#!/usr/bin/env python

import numpy as np
import pandas as pd
import os
import sys
import argparse
import time
import cv2
import re

import matplotlib.pyplot as plt

import caffe
from threading import Thread
from time import sleep

from scipy.misc import imresize

def main(argv):

	pycaffe_dir = os.path.dirname(__file__)

	parser = argparse.ArgumentParser()
	# Optional arguments.
	parser.add_argument(
	    "--model_def",
	    default=os.path.join(pycaffe_dir,
	            "/home/ubuntu/deploy_files/deploy_alexnet_b1.prototxt"),
	    help="Model definition file."
	)
	parser.add_argument(
	    "--pretrained_model",
	    default=os.path.join(pycaffe_dir,
	            "/home/ubuntu/deploy_files/bvlc_alexnet.caffemodel"),
	    help="Trained model weights file."
	)
	parser.add_argument(
	    "--cpu",
	default=False,
	    action='store_true',
	    help="Switch for cpu computation."
	)	
	parser.add_argument(
	    "--mean_file",
	    default=os.path.join(pycaffe_dir,
	                         '/home/ubuntu/deploy_files/imagenet_mean.binaryproto'),
	    help="Data set image mean of [Channels x Height x Width] dimensions " +
	         "(numpy array). Set to '' for no mean subtraction."
	)
	parser.add_argument(
	    "--raw_scale",
	    type=float,
	    default=255.0,
	    help="Multiply raw input by this scale before preprocessing."
	)
	parser.add_argument(
	    "--channel_swap",
	    default='2,1,0',
	    help="Order to permute input channels. The default converts " +
	         "RGB -> BGR since BGR is the Caffe default by way of OpenCV."

	)
	parser.add_argument(
	    "--camera",
	    default="nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720,format=(string)I420, framerate=(fraction)24/1 ! nvvidconv flip-method=2 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink",
	    help="Specify the ID of the device, ex: 1 for /dev/video1, or a gstreamer command."
        )
	parser.add_argument(
	    "--labels_file",
	    default=os.path.join(pycaffe_dir,
	            "/home/ubuntu/deploy_files/synset_words.txt"),
	    help="Readable label definition file."
	)
	args = parser.parse_args()

	mean, channel_swap = None, None
	if args.mean_file:
	   ### How to load a pickle file
	   ### mean = np.load(args.mean_file)
	   data=open(args.mean_file,'rb').read()
	   blob=caffe.proto.caffe_pb2.BlobProto()
	   blob.ParseFromString(data) 
	   mean=np.array(caffe.io.blobproto_to_array(blob))[0,:,:,:]

	   
	if args.channel_swap:
	    channel_swap = [int(s) for s in args.channel_swap.split(',')]

	if args.cpu:
	    caffe.set_mode_cpu()
	    print("CPU mode")
	else:
	    caffe.set_mode_gpu()
	    print("GPU mode")

	classifier = caffe.Net(args.model_def, args.pretrained_model, caffe.TEST)
	transformer = caffe.io.Transformer({'data': classifier.blobs['data'].data.shape})
	#transformer.set_raw_scale('data', 255)
	transformer.set_transpose('data', (2,0,1))
	#transformer.set_channel_swap('data', (2,1,0))
	transformer.set_mean('data',mean.mean(1).mean(1))

	print ""
	print "Reading frames from webcam..."
	print "Using Camera: "+args.camera
	print ""

	# Open stream
	stream = cv2.VideoCapture(args.camera)

        if not stream.isOpened():
                print("Could not open camera")
                sys.exit(1)

	with open(args.labels_file) as f:
		rawlabels = f.read().splitlines()

		labels = [r for r in rawlabels]
		
	semaphore = False
	while semaphore == False:
		(grabbed, frame) = stream.read()
		if grabbed == False:
			print "Error, unable to grab a frame from the camera"
			quit()


		data = transformer.preprocess('data', frame)

		classifier.blobs['data'].data[...] = data 
		start = time.time()
		out = classifier.forward()
		end = (time.time() - start)*1000

		#cv2.rectangle(frame,(5,10),(450,70),(0,0,0),-1)
		#cv2.putText(frame,"FF time: %dms/%dFPS" % (end,1000/end),
		#	(10,30), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2)
		print("Main: Done in %.4f s." % (time.time() - start))
	
		# scores = out['softmax']
		scores = out['prob']
	

		dispcount=5

		maxmatch = scores.argmax()
		sd=sorted(range(len(scores[0,:])),key=lambda x:scores[0,x],reverse=True)

		for j in range(0,dispcount):	
			wlbl=re.sub(r'^\W*\w+\W*','',labels[sd[j]])
			pred="%4.1f%% %s" % (scores[0,sd[j]]*100,wlbl)
			print pred
			position = (10,20+20*j)
				
			cv2.putText(frame,pred, 
				position, cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),1)	

		
		cv2.imshow('test',frame)
		cv2.waitKey(1)

    	if cv2.waitKey(1) & 0xFF == ord('q'):
    		semaphore = True

	cv2.destroyAllWindows()

if __name__ == '__main__':
	main(sys.argv)

