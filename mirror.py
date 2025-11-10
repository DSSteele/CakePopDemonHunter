# This file will be a minimal OpenCV file for mirroring the webcam

print('This is mirror.py')

import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Flip every frame in the horizontal direction
    frame = cv.flip(frame, 1)
    height, width = frame.shape[:2]

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Calculate change in gray
    delta = cv.absdiff(gray, prev_gray)

    # Display text
    cv.putText(frame, str(delta), (50,300),
        cv.FONT_HERSHEY_SIMPLEX,
        2,              # fontScale
        (255,255,255),  # color
        4)              # thickness

    cv.putText(frame, "Hello", (50,100),
        cv.FONT_HERSHEY_SIMPLEX,
        2,              # fontScale
        (132,38,80),    # color
        4)              # thickness

    # Display the resulting frame
    #cv.imshow('frame', gray)
    cv.imshow('frame', frame)

    #Save previous frame
    prev_gray = gray

    # See if user wants to quit
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
