# This file combines mirror.py and playaudio.py with face detection
# to create the full Cake Pop Demon Hunters game

print('This is SteeleCPDH.py')

import numpy as np
import cv2 as cv
import os
import pygame

# get directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
audio_file = os.path.join(script_dir, "golden_parody.mp3")
first = True
score = 0
FONT = cv.FONT_HERSHEY_SIMPLEX
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# start pygame mixer
pygame.mixer.init()
# load and play audio on a loop
pygame.mixer.music.load(audio_file)
pygame.mixer.music.play(-1)

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
    if first:
        prev_gray = gray
        first = False

    # Calculate change in gray
    #delta = cv.absdiff(gray, prev_gray).sum()
    delta = cv.absdiff(gray[0:100, 0:100], prev_gray[0:100, 0:100]).sum()
    cv.rectangle(frame, (0,0), (100,100), (100,100,100), 2)

    # Display text
    cv.putText(frame, str(delta), (50,300),
        FONT,
        2.0,            # fontScale
        (255,255,255),  # color
        4)              # thickness
    cv.putText(frame, f"Score: {score}", (180, 460),
        FONT,
        2.0,            # fontScale
        (255,255,255),  # color
        8)              # thickness
    cv.putText(frame, f"Score: {score}", (180, 460),
        FONT,
        2.0,            # fontScale
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
# and stop playing music
pygame.mixer.music.stop()
cap.release()
cv.destroyAllWindows()
