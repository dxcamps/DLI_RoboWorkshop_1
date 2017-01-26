# Jetson TX1 Preparation

These are the steps to prepare the Jetson TX1 for the workshop.

1. [Applying the JetPack for L4T 2.3.1](#task1)
1. [Installing a Web Browser on the TX1](#task2)
1. [Installing the Code and deploy_files](#task3)
1. [Compiling caffe fp16 and fp32](#task4)
1. [Downloading the AlexNet and GoogLeNet caffe models](#task5)
1. [Testing the models](#task6)
1. [Building the LED circuit](#task7)
1. [Testing the models with the LEDs](#task8)

___

<a name="task1"></a>

## Applying JetPack for L4T 2.3.1

To update your Jetson TX1 to the appropriate Ubuntu version, you need to apply JetPack for L4T 2.3.1.  This will ensure that the TX1 is running correct version of Ubuntu, and that the latest libraries, frameworks and tools have been installed.

The following steps are performed on the TX1 by the JetPack install:
 - Flash 64 Bit OS to TX1 device
 - Push and install 64Bit CUDA on target
 - Push and install GIE on target
 - Push and install 64Bit OpenCV4Tegra on target
 - Push and install 64Bit PerfKit on target
 - Push and install 64Bit cuDNN on target
 - Push and install 64Bit VisionWorks on target
 - Push and install 64Bit VisionWorks SFM on target
 - Push and install 64Bit VisionWorks Tracking on target
 - Cross-compile 64Bit CUDA samples and push to target
 - Push and install MMAPI on target

You can learn more about the JetPack [here](http://docs.nvidia.com/jetpack-l4t/index.html#developertools/mobile/jetpack/l4t/2.3/jetpack_l4t_main.htm)

***JetPack for L4T installation requires an Ubuntu 14 or later host machine as well as the Jetson TX1.  If you are on Windows you may consider using an Ubuntu boot USB, or creating a VMWare Player or VirtualBox virtual machine with Ubuntu installed.  You cannot easily use Hyper-V because part of the installation requires connecting to the TX1 via USB from the Ubuntu host, and Hyper-V does not support USB access from non-windows guests.***

1. Install the JetPack for L4T 2.3.1 by following the instructions in the [Installation Guide](http://docs.nvidia.com/jetpack-l4t/index.html#developertools/mobile/jetpack/l4t/2.3/jetpack_l4t_install.htm) .  _Make sure to include the all of the steps under "**For Jetson TX1 64Bit**"_

___

<a name="task2"></a>

## Installing a Web Browser on the TX1

There are a few steps in this walkthrough that may require access to the web.  We'll start by making sure a web browser is available. 

1. From a terminal window on the TX1 (you can press Ctrl-Alt-T on the TX1 keyboard to open a terminal prompt) run the following commands:

    ```bash
    sudo apt-get update
    ``` 

    and

    ```bash
    sudo apt-get install chromium-browser
    ```
1. Once the install command is complete, you can open the chromium browser by first opening the Ubuntu Dashboard, or "Dash". The dashboard is identified by the Ubunto Icon on the top left corner of the desktop, or you can open it by pressin the `Super` key.  The `Super` key is the `Windows Key` on windows keyboards, or the `Command` key on Macs.

1. Once the dashboard, or "dash" is open, you can type "chromium" to find the browser icon.  While it is visible, you can drag the icon for the chromium browser to the launcher bar on the left of the screen so you can easily access it in the future. 

___

<a name="task3"></a>

## Installing the Code and deploy_files

There are two source code files provided by for the workshop.

1. From the [Google Drive](https://drive.google.com/drive/u/1/folders/0B-wiicg2Oj7nZWtUMzZrZXFGdjg), download the `Code.zip` and `deploy_files.zip` files
     - We need a more publicly accessible path for these
1. Extract `Code.zip` to `/home/ubuntu/Code` (note the upper case "`C`" in the destination folder name of "`Code`")
1. Extract `deploy_files.zip` to `/home/ubuntu/deploy_files`

___

<a name="task4"></a>

## Compiling caffe fp16 and fp32

1. From a terminal prompt on the TX1 (Ctrl-Alt-T), run the following command to install the caffe pre-requisites:

    > **Note**: Make sure to press `y` to allow the installs to occur.

    ```bash
    sudo apt-get install \
      cmake \
      git \
      libboost-all-dev \
      libgflags-dev \
      libgoogle-glog-dev \
      protobuf-compiler \
      libprotobuf-dev \
      libboost-thread1.58-dev \
      libatlas-dev \
      libatlas-base-dev \
      libatlas3-base \
      libhdf5-dev \
      libleveldb-dev \
      liblmdb-dev
    ```

1. Next, make the appropriate symlinks for key libraries:

    ```bash
    sudo ln -s /usr/lib/libsnappy.so.1 /usr/lib/libsnappy.so
    ```

    ```bash
    cd /usr/lib/aarch64-linux-gnu
    sudo ln -s libhdf5_serial.so.*.*.* libhdf5.so
    sudo ln -s libhdf5_serial_hl.so.*.*.* libhdf5_hl.so
    ```

    ```bash
    sudo ldconfig
    ```
1. Compile caffe fp16:

    ```bash
    cd /home/ubuntu/Code/fp16/caffe
    make clean
    make -j4 all
    ```

1. Compile caffe fp32

    ```bash
    cd /home/ubuntu/Code/fp32/caffe
    make clean
    make -j4 all
    ```

___

<a name="task5"></a>

## Downloading the AlexNet and GoogLeNet caffe models

1. On the TX1, in a Terminal Window (Ctrl-Alt-T), change into the `deploy_files1` folder:

    ```bash
    cd /home/ubuntu/deploy_files
    ```

1. Download the GoogLeNet caffe model

    ```bash
    wget http://dl.caffe.berkeleyvision.org/bvlc_googlenet.caffemodel
    ```

1. Then download the AlexNet caffe model

    ```bash
    http://dl.caffe.berkeleyvision.org/bvlc_alexnet.caffemodel
    ```



