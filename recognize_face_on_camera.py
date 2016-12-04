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
import sys

import cv2
import numpy as np

# Read the settings file
with open('settings_for_recognition.json') as settings_file:
    settings = json.load(settings_file)

cap = cv2.VideoCapture(0)

# Load face cascade
face_cascade = cv2.CascadeClassifier(settings['face_cascade_path'])

# Load the model and the person names
modelPath = settings['saved_model_path']
peopleNamePath = settings['name_array_path']

if not os.path.exists(modelPath) or not os.path.exists(peopleNamePath):
    print "First you have to train a model and save it!"
    sys.exit(1)

model = cv2.createEigenFaceRecognizer()
model.load(modelPath)
people = np.load(peopleNamePath)

predictions = []

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret is True:
        #Resize the frame
        # width
        ret = cap.set(3, 640)
        # height
        ret = cap.set(4, 480)

        # We draw on this
        debugFrame = frame

        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            grayFrame,
            scaleFactor=settings["scaleFactor"],
            minNeighbors=settings["minNeighbors"],
            minSize=(50, 50),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

        for face in faces:
            (x, y, w, h) = face
            # Create a bounding box around the face
            cv2.rectangle(debugFrame, (x, y), (x + w, y + h), (225, 0, 0), 1)
            # Crop out the face
            croppedFace = grayFrame[y:y + h, x:x + w]
            croppedFace = cv2.equalizeHist(croppedFace)
            # Resize for the recognition
            croppedFace = cv2.resize(croppedFace, (settings['resize_for_training'], settings['resize_for_training']))
            # Predict the person
            predictedLabel, predictedConfidence = model.predict(croppedFace)
            # Associate the number with a name
            personName = people[predictedLabel]

            text = "I am: {0}; Conf: {1:.2f}".format(personName, predictedConfidence)
            cv2.putText(debugFrame, text, (x - 20, y - 5), cv2.FONT_HERSHEY_PLAIN, 1.1, (0, 0, 225), 1)

        # Display the resulting frame
        cv2.imshow('Press q to quit!', debugFrame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
