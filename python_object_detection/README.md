# Object Detection with Python+Caffe+OpenCV

### Installing BottleNet

Copy the contents of the BottleNet .tar.gz file into a directory called data

### Running BottleNet

The path to Caffe and OpenCV needs to be set:

```
export CAFFE_HOME=/home/ubuntu/Code/fp32
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${CAFFE_HOME}/caffe/build/lib
export PYTHONPATH=${PYTHONPATH}:${CAFFE_HOME}/caffe/python/
```

The demo can be run as:

```
./demo_od.py
```

Sometimes the response of the code is slow enough that OpenCV believes the program has stalled.  The frame rate with 3 bottles in view should be around 0.3 to 0.4 FPS.

