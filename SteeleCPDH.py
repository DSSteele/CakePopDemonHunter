# This file combines mirror.py and playaudio.py with face detection
# to create the full Cake Pop Demon Hunters game

print('This is SteeleCPDH.py')

import numpy as np
import cv2 as cv
import os, pygame, random, time

# get directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
audio_file = os.path.join(script_dir, "golden_parody.mp3")
# game state variables
score = 0
corner = 0
first = True
tl = tr = bl = br = False
CORNER_SPAWN_TIME = 2.0     # seconds
MIDDLE_SPAWN_TIME = 10.0    # seconds
TOUCH_THRESHOLD = 100000
FONT = cv.FONT_HERSHEY_SIMPLEX
# function definitions
def chooseCorner():
    global corner
    corner = random.randint(1,4)
    match corner:
        case 1:
            global tl
            tl = True
        case 2:
            global tr
            tr = True
        case 3:
            global bl
            bl = True
        case 4:
            global br
            br = True

def spawnDemon():
    if tl == True:
        cv.rectangle(frame, (0,0), (80,80), (0,0,0), -1)
        cv.putText(frame, "D", (20,60),
            FONT,
            2.0,            # fontScale
            (0,0,255),      # color
            4)              # thickness
    if tr == True:
        cv.rectangle(frame, (width-80,0), (width,80), (0,0,0), -1)
        cv.putText(frame, "D", (width-60,60),
            FONT,
            2.0,            # fontScale
            (0,0,255),      # color
            4)              # thickness
    if bl == True:
        cv.rectangle(frame, (0,height-80), (80,height), (0,0,0), -1)
        cv.putText(frame, "D", (20,height-20),
            FONT,
            2.0,            # fontScale
            (0,0,255),      # color
            4)              # thickness
    if br == True:
        cv.rectangle(frame, (width-80,height-80), (width,height), (0,0,0), -1)
        cv.putText(frame, "D", (width-60,height-20),
            FONT,
            2.0,            # fontScale
            (0,0,255),      # color
            4)              # thickness

# Create a new OpenCV cascade classifier and
# load the Haar wavelet profile for a face.
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# start pygame mixer
pygame.mixer.init()
# load and play audio on a loop
pygame.mixer.music.load(audio_file)
pygame.mixer.music.play(-1)

lastCornerSpawn = time.time()
lastMiddleSpawn = time.time()

while True:
    now = time.time()
    if not tl and not tr and not bl and not br:
        if now - lastCornerSpawn >= CORNER_SPAWN_TIME:
            chooseCorner()
            lastCornerSpawn = now

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
    delta1 = cv.absdiff(gray[0:80, 0:80], prev_gray[0:80, 0:80]).sum()
    delta2 = cv.absdiff(gray[0:80, 560:640], prev_gray[0:80, 560:640]).sum()
    delta3 = cv.absdiff(gray[380:460, 0:80], prev_gray[380:460, 0:80]).sum()
    delta4 = cv.absdiff(gray[380:460, 560:640], prev_gray[380:460, 560:640]).sum()
    if tl == True and delta1 >= TOUCH_THRESHOLD:
        tl = False
        lastCornerSpawn = now
        score += 1
    if tr == True and delta2 >= TOUCH_THRESHOLD:
        tr = False
        lastCornerSpawn = now
        score += 1
    if bl == True and delta3 >= TOUCH_THRESHOLD:
        bl = False
        lastCornerSpawn = now
        score += 1
    if br == True and delta4 >= TOUCH_THRESHOLD:
        br = False
        lastCornerSpawn = now
        score += 1

    spawnDemon()
    # Detect faces
    # Uses CascadeClassifier member function to create
    # a list of face objects
    faces = face_cascade.detectMultiScale(gray)

    # Draw rectangle around the faces
    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x+w, y+h), (255,255,255), 2)
        cv.rectangle(frame, (x+2, y+2), (x+w-4, y+h-4), (132,38,80), 2)

    # Display text
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
