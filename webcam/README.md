# Configuring Jetson-TX1 for inference using built-in camera 

This assumes that the Code.zip file has been installed on the Jetson-tx1 into /home/ubuntu/Code and deploy_files.zip has been install into /home/ubuntu/deploy_files.

Other assumptions are that the following CUDA packages are installed:

```
sudo apt-get cuda-toolkit libdnn5
sudo ln -s /usr/local/cuda-8.0 /usr/local/cuda
```


### Install Python Dependencies

```
sudo apt-get install cmake git aptitude screen g++ libboost-all-dev \
    libgflags-dev libgoogle-glog-dev protobuf-compiler libprotobuf-dev \
    bc libblas-dev libatlas-dev libhdf5-dev libleveldb-dev liblmdb-dev \
    libsnappy-dev libatlas-base-dev python-numpy libgflags-dev \
    libgoogle-glog-dev python-skimage python-protobuf python-pandas \
    libopencv4tegra-python
```

### Create pycaffe interfaces (separately for fp16 and fp32)
NOTE: Currently works for fp32 only

```
cd /home/ubuntu/Code/fpXX/caffe
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

### Set environment for python interface, this can be either fp16 or fp32

export CAFFE_HOME=/home/ubuntu/Code/fp32
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${CAFFE_HOME}/caffe/build/lib
export PYTHONPATH=${PYTHONPATH}:${CAFFE_HOME}/caffe/python/

### Run the webcam driver

```
cd /home/ubuntu/deploy_files/webcam
python webCamClassify.py
```





