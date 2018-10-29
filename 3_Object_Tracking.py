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

# https://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/
# helpful tutorial

import numpy as np
import cv2
import cv2.cv
import math

cap = cv2.VideoCapture(0) # get video source from pi system's first available camera (0)
cap.set(3,320) # Width # reducing resolution for quick processing
cap.set(4,240) # Height

while(True):

    # FILTER BY COLOUR    
    ret,frame = cap.read() # get the frame from the capture source object (frame), ret isn't used

    # Filtering by HSV colourspace
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert to HSV colourspace

    lower_red = np.array([160,100,100]) # setup lower threshold masks for filtering (H,S,V)
    upper_red = np.array([200,250,200]) # setup upper threshold masks for filtering (H,S,V)
    # use higher than 180 hue to wrap around to 0

    lower = np.array(lower_red, dtype = "uint8") # cast to type that the opencv can process consistently
    upper = np.array(upper_red, dtype = "uint8")

    _mask = cv2.inRange(frame, lower, upper) # find boolean mask for filtering
    frame = cv2.bitwise_and(frame, frame, mask = _mask) # bitwise-and original frame using the mask above to find the filtered frame. 
    
    frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR) # convert filtered frame back to BGR colourspace (opencv likes BGR rather than RGB)



    # CIRCLE DETECTION
    cimg = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) # convert to greyscale colourspace
    
    cimg = cv2.GaussianBlur(cimg, (9,9), 0) # (optional: smooth image to reduce detection errors, must be an odd number)    

    circles = cv2.HoughCircles(cimg, cv2.cv.CV_HOUGH_GRADIENT, 1, 50, param1=40, param2=15, minRadius=1, maxRadius=50)
    # this function will need some tuning and trial & error, see the opencv documentation

    if(circles != None): # if there are circle detected in the frame
        
        circles = np.uint16(np.around(circles))
          
        for i in range(len(circles[0])): # loop through all the circles detected
            # draw the outer circle
            cv2.circle(frame,(circles[0][i][0],circles[0][i][1]),circles[0][i][2],(0,255,0),2)
            # draw the centre of the circle
            cv2.circle(frame,(circles[0][i][0],circles[0][i][1]),2,(0,0,255),3)
            # see documentation for draw functions
        
        # Normalised Co-ordinates and radius
        CircleX = np.around(((circles[0][0][0] - (cap.get(3)/2))/(cap.get(3)/2)),2) 
        CircleY = np.around(((circles[0][0][1] - (cap.get(4)/2))/(cap.get(4)/2)),2)
        CircleRad = np.around((circles[0][0][2])/cap.get(3),3)

        # find angle based on position in the frame and convert radians to degrees
        Degrees = (((math.atan2(CircleX,-CircleY))/(math.pi * 2)) * 360)
        Degrees = np.around(Degrees, 1)

        # find the magnitude of the position vector
        Magnitude = math.sqrt((CircleX*CircleX)+(CircleY*CircleY))
        Magnitude = np.around(Magnitude, 1)

        # overlay text on screen
        cv2.putText(frame, "(Cartesian) " + "X: " + str(CircleX) + " " + "Y: " + str(CircleY), (20,20), cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        cv2.putText(frame, "(Polar) " + "Deg: " + str(Degrees) + " " + "Mag: " + str(Magnitude), (20,40), cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        cv2.putText(frame, "Radius: " + str(CircleRad), (20,60), cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))

    # show frame in a separate window
    cv2.imshow('Tracking',frame)

    # if 'q' key is pressed, program ends
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break        

# release resources
cap.release()
cv2.destroyAllWindows()
