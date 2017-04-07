# Lab 3
The purpose of this lab is to execute object detection on an image. We will provide an image for a trained model where a python app is able to detect 
this object based on the trained model we have completed on Azure VM in the prep work step.


1. We will create a folder named "bottlenet" inside "detection" folder. Run the following command: 

    ```
    cd ~/detection; mkdir bottlenet
    ```

2. We will extract  the trained model in zip file 'bottlenet.tgz' located at the home directory to the 'bottlenet' folder:

    ```
    cd bottlenet; tar xzf ~/bottlenet.tgz
    ```

    This simulates downloading model from Azure and deploying

4. Run object detection for 'sodagroup.jpg' file by executing the following command:

    ```
    ./imageDetect.py sodagroup.jpg
    ```

    You should see a single LED turn on
