# Build and run the BottleNet Object Detection Inference Demo

## Prerequisites

The GIE library must be installed.  The rest of the prerequisites will be installed by cmake when building the jetson-inference package.

### Install GIE

This should have been satisfied when you installed the software on the Jetson.  If not, transfer the package nv-gie-repo-ubuntu1604-6-rc-cuda8.0_1.0.2-1_arm64.deb from JetPack download.  

```
sudo dpkg -i nv-gie-repo-ubuntu1604-6-rc-cuda8.0_1.0.2-1_arm64.deb
sudo apt-get install libgie-dev
```

## Download jetson-inference repository

```
git clone  https://github.com/dusty-nv/jetson-inference
```

## Apply the BottleNet patch

```
patch -p0 < bottlenet.patch
```

## Install the BottleNet Data

TODO.  
```
mkdir data/networks/bottlenet
pushd data/networks/bottlenet
pushd
cd jetson-inference/data/networks
wget TODO
tar -xzvf 20170110-230207-dc14_epoch_100.0.tar.gz
popd
```

## Remove the Python layer from the BottleNet deploy network

```
patch -p0 < ../../../../deploy_bottlenet.patch
```

## Build Jetson-Inference

Running cmake will download all of the models and data required by jetson-inference.  The process will take 10-15 minutes depending on your internet connection.

```
mkdir build
cd build
cmake ..
make -j4
```

### Run the Demo

The first time you run the demo, it will take a few minutes for the program to build the network.

```
cd aarch64/bin
./detectnet-camera bottlenet
```





