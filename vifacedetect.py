# This program will capture video from webcam,
# perform face detection, then display webcam on screen
# with a bounding box around detected faces.

import cv2

# Create a new OpenCV cascade classifier and
# load the Haar wavelet profile for a face.
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Use OpenCV to open connection to any capture device.
cap = cv2.VideoCapture(cv2.CAP_ANY)

# 
# To use a video file as input
# cap = cv2.VideoCapture('filename.mp4')

# If there is an error getting a camera, print error.
if not cap.isOpened():
    print('Cannot open camera. Make sure you have a webcam, ')
    print("and that it's not being used by another app.")
    exit()

# Loop forever (unless there is a break)
while True:

    # Read the frame (the tensor image ndarray)
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Error reading frame. Exiting ...")

    # Display

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    # Uses CascadeClassifier member function to create
    # a list of face objects
    faces = face_cascade.detectMultiScale(gray)

    # Prints coordinates of all detected faces, if any
    print('detected face(s) at:', faces)

    # Draw rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 5)
        cv2.rectangle(frame, (x-5, y-5), (x+w+10, y+h+10), (0, 0, 0), 5)

    cv2.imshow('q to quit', frame)
    # Stop if q key is pressed
    if cv2.waitKey(30) == ord('q'):
        break
# Release the VideoCapture object
cap.release()
cv2.destroyAllWindows()
