# Configuring Jetson-TX1 for inference using built-in camera 

This assumes that the Code.zip file has been installed on the Jetson-tx1 into /home/ubuntu/Code and deploy_files.zip has been install into /home/ubuntu/deploy_files.

Other assumptions are that the following CUDA packages are installed:

```
sudo apt-get cuda-toolkit libdnn5
sudo ln -s /usr/local/cuda-8.0 /usr/local/cuda
```

## Install GStreamer-1.0
```
sudo add-apt-repository universe 
sudo add-apt-repository multiverse 
sudo apt-get update 
sudo apt-get install gstreamer1.0-tools gstreamer1.0-alsa gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav 
sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-good1.0-dev libgstreamer-plugins-bad1.0-dev 
```

## Install Python Dependencies

```
sudo apt-get install cmake git aptitude screen g++ libboost-all-dev \
    libgflags-dev libgoogle-glog-dev protobuf-compiler libprotobuf-dev \
    bc libblas-dev libatlas-dev libhdf5-dev libleveldb-dev liblmdb-dev \
    libsnappy-dev libatlas-base-dev python-numpy libgflags-dev \
    libgoogle-glog-dev python-skimage python-protobuf python-pandas \
    libopencv4tegra-python
```

### Installing OpenCV 3.2

This is needed for GSTREAMER to work with the Jetson Camera.

It is highly desirable that you have removed any system OpenCV and used this one.  If this is your own machine and you have built OpenCV by hand, you can probably skip this step.  The default with Ubuntu may not be adequate.

You need about 7GB of space on the local disk to built this.  Either clean up aggressively, install this before installing the rest of the large files, or install a MicroSD card or USB drive and work on that.

This procedure follows the ones found at: https://devtalk.nvidia.com/default/topic/983098/jetson-tx1/opencv-3-1-with-usb-camera-support/

```
sudo apt-get install build-essential
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
sudo apt-get install python2.7-dev
sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
sudo apt-get install libgtkglext1 libgtkglext1-dev
sudo apt-get install qtbase5-dev
sudo apt-get install libv4l-dev v4l-utils qv4l2 v4l2ucp
git clone https://github.com/opencv/opencv.git
mkdir release
cd release
cmake -D WITH_CUDA=ON -D CUDA_ARCH_BIN="5.3" -D CUDA_ARCH_PTX="" -D WITH_OPENGL=ON -D WITH_LIBV4L=ON -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ..
make -j8
sudo make install
cd ../..

```
## Create pycaffe interfaces (separately for fp16 and fp32)
NOTE: Currently works for fp32 only.  This might rebuild the entire application.

### For FP32
```
cd /home/ubuntu/Code/fp32/caffe
```
Add the path for the AARCH64 target of CUBLAS to Makefile.config. This requires adding the path to the INCLUDE_PATH and LIBRARY_PATH variables.  They should look like:

```
INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include /usr/include/hdf5/serial/ /usr/local/cuda-8.0/targets/aarch64-linux/include/
LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib /usr/lib/aarch64-linux-gnu/hdf5/serial/ /usr/local/cuda-8.0/targets/aarch64-linux/lib
```

Then build the interface.  This may trigger a complete rebuild of caffe depending on the state of your build.
```
make -j3 pycaffe
```

### For FP16

## Set environment for python interface, this can be either fp16 or fp32

```
export CAFFE_HOME=/home/ubuntu/Code/fp32
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${CAFFE_HOME}/caffe/build/lib
export PYTHONPATH=${PYTHONPATH}:${CAFFE_HOME}/caffe/python/
```

## Run the webcam driver

By default, it is going to use the AlexNet config files found in the deploy_files directory. 

```
cd /home/ubuntu/DLI_RoboWorkshop_1/webcam
python webCamClassify.py
```

If you want to use the CPU mode, add the flag --with-cpu

By default, this will use the built-in camera.  If you want to change the camera to use another USB camera, specify the device, ex: --camera="/dev/video1".  If you were so inclined, you could add a GStreamer-1.0 command as the camera.  See the code for how this can be done.  In theory, you could specify a .mp4 file as the camera and it will stream through that.

If you want to use the GoogleNet model, you can specify that via the command line:

```
cd /home/ubuntu/DLI_RoboWorkshop_1/webcam
python webCamClassify.py --model_def /home/ubuntu/deploy_files/deploy_googlenet_b1.prototxt --pretrained_model /home/ubuntu/deploy_files/bvlc_googlenet.caffemodel
```



