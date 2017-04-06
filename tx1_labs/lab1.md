
# Lab 1
The purpose of this lab is to execute static classification commands for a given set of images using 3 LEDs circuit.


1. Open a terminal on the Jetson, Run the following command:

'''
sudo /etc/rc.local to prep LEDs (password is ubuntu)
'''

2. Go to classification folder, Run the following command:

'''
cd ~/classification
'''

3. Run the following commands to classify set of images (apple, lemon, banana and nvidia):

'''
 ./static_classify.sh grannysmith.jpg
'''
Output: You should see LED0 light up

'''
 ./static_classify.sh lemon.jpg
'''
Output: You should see LED1 light up

'''
 ./static_classify.sh banana.jpg
'''
Output: You should see LED2 light up


'''
 ./static_classify.sh nvidia.jpg
'''
Output: You should see all LEDs shut off

Would you know why this happened? 
The program was not able to classify 'nvidia.jpg' image, therefore no LED will light on.

[Lab 1 commands](/images/lab1Commands.jpg)