# Lab 2
The purpose of this lab is to execute live camera classification commands for Jetson TX1 built in camera.


1. Make sure you are still in the classification folder, if not execute the below command:

    ```
    cd ~/classification
    ```

2. Execute the following command to run webCamClassify python file:

    ```
    Run ./webCamClassify.py
    ```
    
    This will turn on live video for the built in camera in Jetson TX1. The status of the camera is trying to recognize any of the objects in the
    current scene. Likely won’t see any LEDs light up initially (no recognized objects).

3. Jetson TX1 contains a file named 'synset_words.txt' in the classification folder. Try to double click on this file and look for any class ids that you have in hand or around you such as: a computer mouse,a water bottle, etc. Find IDs with their associated class names in synset_words.txt

    ![words file](/tx1_labs/images/words_classes.png)

4. Modify webCamClassify.py and change the object IDs to be identified by the camera such as a water bottle.

    a. Open webCamClassify.py file.

    b. Edit 'toggleLEDs' function.

    c. Add class for any object you can present to the live camera in Jetson TX1. Try using “computer mouse” or “water bottle” or “bottle cap”.

    d. Save the file.


    Below is a sample code of the edited toggle LEDS method in Python, feel free you select any other class in this function.
    
    ![Toggle LEDs function](/tx1_labs/images/toggleLEDs.png)

5. Re-run webClassify file.

    ```
    ./webCamClassify.py
    ```

    Should see associated LEDs light up when holding up recognized object

