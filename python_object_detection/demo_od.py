#!/usr/bin/env python

import time
import os
import sys
import cv2
import caffe
import numpy as np

default_camera="nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720,format=(string)I420, framerate=(fraction)24/1 ! nvvidconv flip-method=2 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"

inputdev=default_camera

# Configure Caffe to use the GPU for inference
caffe.set_mode_gpu()

MODEL_DIR="data/"
last_iteration='37300'


# Load the dataset mean image file
#mean = np.load('data/mean.binaryproto')

b = caffe.proto.caffe_pb2.BlobProto()
data = open(MODEL_DIR+'mean.binaryproto','rb').read()
b.ParseFromString(data)
mean = np.array(caffe.io.blobproto_to_array(b))[0]

mean=np.swapaxes(mean,0,2)
mean=np.swapaxes(mean,0,1)


# Instantiate a Caffe model in GPU memory
# The model architecture is defined in the deploy.prototxt file
# The pretrained model weights are contained in the snapshot_iter_<number>.caffemodel file
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

loop=True
cval=True
pause=False

while loop:
    # Create opencv video object
    vid = cv2.VideoCapture(inputdev)

    while(vid.isOpened()):
        ret, frame = vid.read()

	height_input=frame.shape[0]
	width_input=frame.shape[1]
        od_frame=cv2.resize(frame,(WIDTH,HEIGHT),0,0)
    
        t1 = time.time()

        data = transformer.preprocess('data', od_frame.astype('float16')/255)
        # Set the preprocessed frame to be the Caffe model's data layer
        classifier.blobs['data'].data[...] = data
        # Measure inference time for the feed-forward operation
        # The output of DetectNet is an array of bounding box predictions
        bounding_boxes = classifier.forward()['bbox-list'][0]

        dt = (time.time() - t1)
    
        if cval:
            # Convert the image from OpenCV BGR format to matplotlib RGB format for display
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
               
            # Create a copy of the image for drawing bounding boxes
            overlay = frame.copy()
               
            # Loop over the bounding box predictions and draw a rectangle for each bounding box
            for bbox in bounding_boxes:
                if  bbox.sum() > 0:
                # Scale the bboxes to the output size
                    b0=np.int(bbox[0]/WIDTH*width_input)
                    b1=np.int(bbox[1]/HEIGHT*height_input)
                    b2=np.int(bbox[2]/WIDTH*width_input)
                    b3=np.int(bbox[3]/HEIGHT*height_input)

                    cv2.rectangle(overlay, (b0,b1), (b2,b3), (255, 0, 0), -1)
             
                # Overlay the bounding box image on the original image
                frame = cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        else:
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            # scale up to make it more white
            gray=127+np.rint(gray/2)
                 
            gframe=np.copy(frame)
            gframe[:,:,0]=gray
            gframe[:,:,1]=gray
            gframe[:,:,2]=gray

                # Loop over the bounding boxes and copy the colored section into the overlay
            for bbox in bounding_boxes:
                if  bbox.sum() > 0:
            #  Scale the bboxes to the output size
                    b0=np.int(bbox[0]/WIDTH*width_input)
                    b1=np.int(bbox[1]/HEIGHT*height_input)
                    b2=np.int(bbox[2]/WIDTH*width_input)
                    b3=np.int(bbox[3]/HEIGHT*height_input)

                    gframe[b1:b3,b0:b2,:]=frame[b1:b3,b0:b2,:]

            frame=gframe
      
        #itxt="Inference time: %dms per frame" % end 
        #        
        ## Display the inference time per frame
        #cv2.putText(frame,itxt,
        #            (10,height_input-60), cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
  
	print "inference time=%.3f ms, total time per frame=%.3f ms" % (1000*dt,1000*(time.time()-t1)) 
	cv2.imshow('object detection',frame)
        wtstr="%4.1f FPS" % (1.0/dt)
        cv2.setWindowTitle('object detection', wtstr)


        # Now check the keypresses to do something different
        v=cv2.waitKey(1)
        if (v & 0xFF) == ord('q'):
            break
        if (v & 0xFF) == ord('g'):
            cval=not cval
        if (v & 0xFF) == ord('s'):
            pause=not pause
	if (v & 0xFF) == ord('q'):
	    loop=False

    vid.release()


cv2.destroyAllWindows()


