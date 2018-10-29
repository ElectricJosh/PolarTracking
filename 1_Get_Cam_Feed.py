# Prerequisites:

# make sure your camera is recognised and enabled on your system, common USB webcams are usually ok but picam may need some setup.
# goto start>Preferences>Rapberry Pi Configuration>Interfaces (tab) --> Enable camera
# picam may also need further drivers installed, like the picamera library

# Also helpful
#https://www.raspberrypi.org/forums/viewtopic.php?t=176697
#sudo modprobe bcm2835-v4l2

# This code runs on the opencv framework for python, use the bash prompt to download and install.
# I used the SimpleCV tutorial as it was easier to do in one go.

#https://github.com/sightmachine/SimpleCV/blob/develop/doc/HOWTO-Install%20on%20RaspberryPi.rst
# if this fails use "--no-cache-dir" to stop pip error

import numpy as np
import cv2

cap = cv2.VideoCapture(0) # get video source from pi system's first available camera (0)

# reducing resolution for quick processing
cap.set(3,320) # Width 
cap.set(4,240) # Height

while(True):
    ret,frame = cap.read() # get the frame from the capture source object (frame), ret isn't used
    
    cv2.imshow('frame',frame) # create window showing captured frame
    if cv2.waitKey(1) & 0xFF == ord('q'): # press q to quit window
        break
    
cap.release() # release video object feed
cv2.destroyAllWindows() # get rid of windows
