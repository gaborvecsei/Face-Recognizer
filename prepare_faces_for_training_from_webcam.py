"""
/*****************************************************
 *
 *              Gabor Vecsei
 * Email:       vecseigabor.x@gmail.com
 * Blog:        https://gaborvecsei.wordpress.com/
 * LinkedIn:    www.linkedin.com/in/vecsei-gabor
 * Github:      https://github.com/gaborvecsei
 *
 *****************************************************/
"""

import json
import os

import cv2

# Read the settings file
with open('settings_for_recognition.json') as settings_file:
    settings = json.load(settings_file)

# When we run it without custom args read from the settings json config file
outputFolderPath = settings['output_folder']

# Who is the person...
personName = ""
nameInput = raw_input("Please enter the peron's name:	")

# Create the output folder
outputPath = os.path.join(outputFolderPath, nameInput)
# If we don't have the output folder with the correct name, we have to make it
if not os.path.exists(outputPath):
    os.makedirs(outputPath)

# Loading the face cascade
face_cascade = cv2.CascadeClassifier(settings['face_cascade_path'])

cap = cv2.VideoCapture(0)
number = 0

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret is True:
        debugFrame = frame
        grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect the faces
        faces = face_cascade.detectMultiScale(
            grayImage,
            scaleFactor=settings["scaleFactor"],
            minNeighbors=settings["minNeighbors"],
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

        # Crop out and save faces
        for face in faces:
            (x, y, w, h) = face
            if cv2.waitKey(1) & 0xFF == ord('k'):
                # Crop out the face
                croppedFace = frame[y:y + h, x:x + w]
                # Save the face to the output folder
                number += 1
                fullImagePath = outputPath + "/" + str(number) + "_.jpg"
                cv2.imwrite(fullImagePath, croppedFace)
                print "Face detected and cropped: " + fullImagePath
            cv2.rectangle(debugFrame, (x, y), (x + w, y + h), (225, 0, 0), 1)

        # Display the resulting frame
        cv2.imshow('Press k to save detection! Press q to quit.', debugFrame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
