# Jetson TX1 Preparation

These are the steps to prepare the Jetson TX1 for the workshop.

1. [Applying the JetPack for L4T 2.3.1](#task1)
1. [Installing a Web Browser on the TX1](#task2)
1. [Installing the Code and deploy_files](#task3)
1. [Compiling caffe fp16 and fp32](#task4)
1. [Downloading the AlexNet and GoogLeNet caffe models](#task5)
1. [Testing caffe](#task6)
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
    cd /usr/lib/aarch64-linux-gnu
    sudo ln -s libhdf5_serial.so.*.*.* libhdf5.so
    sudo ln -s libhdf5_serial_hl.so.*.*.* libhdf5_hl.so
    sudo ln -s libsnappy.so.*.*.* libsnappy.so
    sudo ldconfig
    ```

1. You can verify the symlinks you just created, by running the following commands, and verify that the symlinks are pointing to a specific version of their corresponding libraries:

    ```bash
    readlink -f /usr/lib/aarch64-linux-gnu/libhdf5.so
    readlink -f /usr/lib/aarch64-linux-gnu/libhdf5_hl.so
    readlink -f /usr/lib/aarch64-linux-gnu/libsnappy.so
    ```

    Example executions and outputs (your versions may be different as time goes on):

    ```bash
    ~$ readlink -f /usr/lib/aarch64-linux-gnu/libhdf5.so
    /usr/lib/aarch64-linux-gnu/libhdf5_serial.so.10.1.0

    ~$ readlink -f /usr/lib/aarch64-linux-gnu/libhdf5_hl.so
    /usr/lib/aarch64-linux-gnu/libhdf5_serial_hl.so.10.0.2

    ~$ readlink -f /usr/lib/aarch64-linux-gnu/libsnappy.so
    /usr/lib/aarch64-linux-gnu/libsnappy.so.1.3.0
    ```

1. You can set the clocks on the Jetson TX1 to max speed to help decrease compiliation time by running the following command:

    > **Note**: After you run the script, you should notice that the CPU fan on the TX1 is turned on if it wasn't already running. 

    ```bash
    sudo ~/jetson_clocks.sh
    ```

1. Compile caffe fp16:

    > **Note**: This could take 10 minutes or longer to complete.  You will also likey see a number of `nvcc warning:` messages.  These can be safely ignored.

    ```bash
    cd /home/ubuntu/Code/fp16/caffe
    make clean
    make -j4 all
    ```

1. Compile caffe fp32

    > **Note**: This could take 12 minutes or longer to complete.  You will also likey see a number of `nvcc warning:` messages.  These can be safely ignored.

    ```bash
    cd /home/ubuntu/Code/fp32/caffe
    make clean
    make -j4 all
    ```

___

<a name="task5"></a>

## Downloading the GoogLeNet and AlexNet caffe models

1. On the TX1, in a Terminal Window (Ctrl-Alt-T), change into the `deploy_files` folder:

    ```bash
    cd /home/ubuntu/deploy_files
    ```

1. Download the GoogLeNet caffe model

    > **Note**: This is a 51MB file and will take a minute or two or longer to download depending on the speed of your network.

    ```bash
    wget http://dl.caffe.berkeleyvision.org/bvlc_googlenet.caffemodel
    ```

1. Then download the AlexNet caffe model

    > **Note**: This is a 233MB file and will five to six minutes or longer to download depending on the speed of your network.

    ```bash
    wget http://dl.caffe.berkeleyvision.org/bvlc_alexnet.caffemodel
    ```
___

<a name="task6"></a>

## Testing caffe

1. On the TX1, in a Terminal Window (Ctrl-Alt-T),  test the fp16 caffe build by running the following commands:

    - First test to see if it can identify a banana from a static banana.jpg image:

        ```bash
        ~/Code/fp16/caffe/build/examples/cpp_classification/classification.bin \
          /home/ubuntu/deploy_files/deploy.prototxt \
          /home/ubuntu/deploy_files/bvlc_alexnet.caffemodel \
          /home/ubuntu/deploy_files/imagenet_mean.binaryproto \
          /home/ubuntu/deploy_files/synset_words.txt \
          /home/ubuntu/deploy_files/banana.jpg
        ```

        Sample output (notice that banana was the top guess, with a .9996 confidence level):

        ```bash
        ---------- Prediction for /home/ubuntu/deploy_files/banana.jpg ----------
        0.9996 - "n07753592 banana"
        0.0002 - "n03786901 mortar"
        0.0000 - "n07749582 lemon"
        0.0000 - "n03775546 mixing bowl"
        0.0000 - "n01945685 slug"
        ```

    - Next, test a lemonfrom the static lemon.jpg image:

        ```bash
        ~/Code/fp16/caffe/build/examples/cpp_classification/classification.bin \
          /home/ubuntu/deploy_files/deploy.prototxt \
          /home/ubuntu/deploy_files/bvlc_alexnet.caffemodel \
          /home/ubuntu/deploy_files/imagenet_mean.binaryproto \
          /home/ubuntu/deploy_files/synset_words.txt \
          /home/ubuntu/deploy_files/lemon.jpg
        ```

        Sample output (notice that lemon was the top guess, with a .9642 confidence level):

        ```bash
        ---------- Prediction for /home/ubuntu/deploy_files/lemon.jpg ----------
        0.9642 - "n07749582 lemon"
        0.0321 - "n07747607 orange"
        0.0023 - "n07716906 spaghetti squash"
        0.0005 - "n03134739 croquet ball"
        0.0002 - "n04409515 tennis ball"
        ```

    - Finally, test to see if it can identify a granny smith apple from the static grannysmith.jpg image:

        ```bash
        ~/Code/fp16/caffe/build/examples/cpp_classification/classification.bin \
          /home/ubuntu/deploy_files/deploy.prototxt \
          /home/ubuntu/deploy_files/bvlc_alexnet.caffemodel \
          /home/ubuntu/deploy_files/imagenet_mean.binaryproto \
          /home/ubuntu/deploy_files/synset_words.txt \
          /home/ubuntu/deploy_files/grannysmith.jpg
        ```

        Sample output (notice that "Granny Smith" was the top guess, with a .9998 confidence level):

        ```bash
        ---------- Prediction for /home/ubuntu/deploy_files/grannysmith.jpg ----------
        0.9998 - "n07742313 Granny Smith"
        0.0002 - "n07753113 fig"
        0.0000 - "n07749582 lemon"
        0.0000 - "n12267677 acorn"
        0.0000 - "n07716906 spaghetti squash"
        ```

1. Next, test the fp32 caffe build by running the following commands:

    > **Note**: These are the same commands we ran to test the fp16 build, but simply pointed at the fp32 build instead.

    - First test to see if it can identify a banana from a static banana.jpg image:

        ```bash
        ~/Code/fp32/caffe/build/examples/cpp_classification/classification.bin \
          /home/ubuntu/deploy_files/deploy.prototxt \
          /home/ubuntu/deploy_files/bvlc_alexnet.caffemodel \
          /home/ubuntu/deploy_files/imagenet_mean.binaryproto \
          /home/ubuntu/deploy_files/synset_words.txt \
          /home/ubuntu/deploy_files/banana.jpg
        ```

        Sample output (notice that banana was the top guess, with a .9996 confidence level):

        ```bash
        ---------- Prediction for /home/ubuntu/deploy_files/banana.jpg ----------
        0.9996 - "n07753592 banana"
        0.0002 - "n03786901 mortar"
        0.0000 - "n07749582 lemon"
        0.0000 - "n03775546 mixing bowl"
        0.0000 - "n01945685 slug"
        ```

    - Next, test a lemonfrom the static lemon.jpg image:

        ```bash
        ~/Code/fp32/caffe/build/examples/cpp_classification/classification.bin \
          /home/ubuntu/deploy_files/deploy.prototxt \
          /home/ubuntu/deploy_files/bvlc_alexnet.caffemodel \
          /home/ubuntu/deploy_files/imagenet_mean.binaryproto \
          /home/ubuntu/deploy_files/synset_words.txt \
          /home/ubuntu/deploy_files/lemon.jpg
        ```

        Sample output (notice that lemon was the top guess, with a .9642 confidence level):

        ```bash
        ---------- Prediction for /home/ubuntu/deploy_files/lemon.jpg ----------
        0.9642 - "n07749582 lemon"
        0.0321 - "n07747607 orange"
        0.0023 - "n07716906 spaghetti squash"
        0.0005 - "n03134739 croquet ball"
        0.0002 - "n04409515 tennis ball"
        ```

    - Finally, test to see if it can identify a granny smith apple from the static grannysmith.jpg image:

        ```bash
        ~/Code/fp32/caffe/build/examples/cpp_classification/classification.bin \
          /home/ubuntu/deploy_files/deploy.prototxt \
          /home/ubuntu/deploy_files/bvlc_alexnet.caffemodel \
          /home/ubuntu/deploy_files/imagenet_mean.binaryproto \
          /home/ubuntu/deploy_files/synset_words.txt \
          /home/ubuntu/deploy_files/grannysmith.jpg
        ```

        Sample output (notice that "Granny Smith" was the top guess, with a .9998 confidence level):

        ```bash
        ---------- Prediction for /home/ubuntu/deploy_files/grannysmith.jpg ----------
        0.9998 - "n07742313 Granny Smith"
        0.0002 - "n07753113 fig"
        0.0000 - "n07749582 lemon"
        0.0000 - "n12267677 acorn"
        0.0000 - "n07716906 spaghetti squash"
        ```
