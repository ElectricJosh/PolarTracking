# This program finds the HSV values from the centre pixel from a camera feed.
# uses a red-dot reticle to find the object to extract colour components from.

import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0) # get video source from pi system's first available camera (0)
cap.set(3,320) # Width # reducing resolution for quick processing
cap.set(4,240) # Height

while(True):
    ret,frame = cap.read() # get the frame from the capture source object (frame), ret isn't used

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert to HSV colourspace

    CH_H, CH_S, CH_V = cv2.split(frame) # find the Hue, Saturation, Value components of the frame

    _center1 = np.uint16(np.round(cap.get(3)/2)) # find the horizontal centre pixel
    _center2 = np.uint16(np.round(cap.get(4)/2)) # find the vertical centre pixel

    _target = frame # creates duplicate frame for finding colour target

    cv2.circle(_target,(_center1,_center2),2,(0,0,255),3)
    # apply a red dot to the centre of the frame so the user can target the object to find HSV components from.
    
    cv2.imshow('Camera',_target)
    # show targeting frame in a window

    # if 'q' key is pressed, program ends
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

pxl_H = CH_H[int(((cap.get(3))/2)),int(((cap.get(4))/2))] # find Hue value of middle pixel
pxl_S = CH_S[int(((cap.get(3))/2)),int(((cap.get(4))/2))] # find Saturation value of middle pixel
pxl_V = CH_V[int(((cap.get(3))/2)),int(((cap.get(4))/2))] # find intensity value of middle pixel

# release resources
cap.release()
cv2.destroyAllWindows()

# print latest values to prompt on exit
print "End"
print(pxl_H)
print(pxl_S)
print(pxl_V)
