# This file combines mirror.py and playaudio.py with face detection
# to create the full Cake Pop Demon Hunters game

print('This is SteeleCPDH.py')

import cv2 as cv
import numpy as np
import os, pygame, random, time

# Get audio from current directory
script_dir = os.path.dirname(os.path.abspath(__file__))
audio_file = os.path.join(script_dir, "golden_parody.mp3")

# Game state variables
score = 0
corner = 0
first = True
middleY = -480
endText = False
gameOver = False
tl = tr = bl = br = False
faceX = faceY = faceW = faceH = 0
CORNER_SPAWN_TIME = 2.0  # seconds
TOUCH_THRESHOLD = 50000  # sensitivity
FONT = cv.FONT_HERSHEY_SIMPLEX

# Corner selection
def chooseCorner():
    global corner, tl, tr, bl, br
    corner = random.randint(1, 4)
    match corner:
        case 1:
            tl = True
        case 2:
            tr = True
        case 3:
            bl = True
        case 4:
            br = True

# Draw corner demon boxes
def spawnDemon():
    if tl:
        cv.rectangle(frame, (0, 0), (80, 80), (0, 0, 0), -1)
        cv.putText(frame, "D", (20, 60), FONT,
            2.0,            # fontScale
            (0, 0, 255),    # color
            4)              # thickness
    if tr:
        cv.rectangle(frame, (width-80, 0), (width, 80), (0, 0, 0), -1)
        cv.putText(frame, "D", (width-60, 60), FONT,
            2.0,            # fontScale
            (0, 0, 255),    # color
            4)              # thickness
    if bl:
        cv.rectangle(frame, (0, height-80), (80, height), (0, 0, 0), -1)
        cv.putText(frame, "D", (20, height-20), FONT,
            2.0,            # fontScale
            (0, 0, 255),    # color
            4)              # thickness
    if br:
        cv.rectangle(frame, (width-80, height-80), (width, height), (0, 0, 0), -1)
        cv.putText(frame, "D", (width-60, height-20), FONT,
            2.0,            # fontScale
            (0, 0, 255),    # color
            4)              # thickness

# Create new OpenCV cascade classifier; load Haar wavelet profile for face
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Setup music and timer
pygame.mixer.init()
pygame.mixer.music.load(audio_file)
pygame.mixer.music.play(-1)
stopwatch = time.time()

# Main game loop
while True:
    now = time.time()

    # quit logic
    if gameOver:
        break
    if endText:
        gameOver = True

    # capture frame-by-frame
    ret, frame = cap.read()

    # flip every frame in the horizontal direction
    frame = cv.flip(frame, 1)
    height, width = frame.shape[:2]

    # if frame is read correctly, ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    if first:
        prev_gray = gray
        first = False

    # calculate change in grayscale in each corner
    delta1 = cv.absdiff(gray[0:80, 0:80], prev_gray[0:80, 0:80]).sum()
    delta2 = cv.absdiff(gray[0:80, 560:640], prev_gray[0:80, 560:640]).sum()
    delta3 = cv.absdiff(gray[400:480, 0:80], prev_gray[400:480, 0:80]).sum()
    delta4 = cv.absdiff(gray[400:480, 560:640], prev_gray[400:480, 560:640]).sum()

    # show score text
    cv.putText(frame, f"Score: {score}", (180, 460), FONT,
        2.0,                # fontScale
        (255, 255, 255),    # color
        8)                  # thickness
    cv.putText(frame, f"Score: {score}", (180, 460), FONT,
        2.0,                # fontScale
        (132, 38, 80),      # color
        4)                  # thickness

    # detect faces
    faces = face_cascade.detectMultiScale(gray)
    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
        cv.rectangle(frame, (x+2, y+2), (x+w-4, y+h-4), (132, 38, 80), 2)
        faceX = x
        faceY = y
        faceW = x + w
        faceH = y + h

    # spawn corner demons
    if not (tl or tr or bl or br):
        if now - stopwatch >= CORNER_SPAWN_TIME:
            chooseCorner()
            stopwatch = now
    spawnDemon()

    # corner demon interactions
    if tl and delta1 >= TOUCH_THRESHOLD:
        tl = False
        stopwatch = now
        score += 1
    if tr and delta2 >= TOUCH_THRESHOLD:
        tr = False
        stopwatch = now
        score += 1
    if bl and delta3 >= TOUCH_THRESHOLD:
        bl = False
        stopwatch = now
        score += 1
    if br and delta4 >= TOUCH_THRESHOLD:
        br = False
        stopwatch = now
        score += 1

    # moving middle demon
    cv.rectangle(frame, (280, middleY), (360, middleY+80), (0, 0, 0), -1)
    cv.putText(frame, "D", (300, middleY+60), FONT,
        2.0,            # fontScale
        (0, 0, 255),    # color
        4)              # thickness
    if middleY <= 480:
        middleY += 5
    else:
        middleY = -480
        score += 5

    # collision with face
    if (faceX < 360 and faceW > 280) and (faceY < middleY+80 and faceH > middleY):
        endText = True

    # see if user wants to quit
    if cv.waitKey(1) == ord('q'):
        endText = True

    # show game over text
    if endText:
        cv.putText(frame, "GAME OVER", (140, 240), FONT,
            2.0,                # fontScale
            (255, 255, 255),    # color
            8)                  # thickness
        cv.putText(frame, "GAME OVER", (140, 240), FONT,
            2.0,                # fontScale
            (132, 38, 80),      # color
            4)                  # thickness

    # display the resulting frame
    cv.imshow('Cake Pop Demon Hunters', frame)

    # save previous frame
    prev_gray = gray

# When everything done, release the capture
pygame.mixer.music.stop()
time.sleep(2)
cap.release()
cv.destroyAllWindows()
