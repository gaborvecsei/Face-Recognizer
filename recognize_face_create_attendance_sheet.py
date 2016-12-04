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

import datetime
import json
import time
import os
import sys

import cv2
import numpy as np
import pandas as pd

# Read the settings file
with open('settings_for_recognition.json') as settings_file:
    settings = json.load(settings_file)

cap = cv2.VideoCapture(0)

# Load face cascade
face_cascade = cv2.CascadeClassifier(settings['face_cascade_path'])
# Load the created model and the people name array to know which label is which name

modelPath = settings['saved_model_path']
peopleNamePath = settings['name_array_path']

if not os.path.exists(modelPath) or not os.path.exists(peopleNamePath):
    print "First you have to train a model and save it!"
    sys.exit(1)

model = cv2.createEigenFaceRecognizer()
model.load(modelPath)
people = np.load(peopleNamePath)

predictions = []
accuracy_number = settings['predictionAccuracyNumber']
accurate_predictions = set()
attendance_sheet_dict = {}

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret is True:
        # Change width and height
        # width
        ret = cap.set(3, 640)
        # height
        ret = cap.set(4, 480)

        # We draw on this and show this to the user
        debugFrame = frame

        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces on image
        faces = face_cascade.detectMultiScale(
            grayFrame,
            scaleFactor=settings["scaleFactor"],
            # For more accurate detection increase this
            minNeighbors=settings["minNeighbors"],
            minSize=(50, 50),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

        # Iterate thru detections
        for face in faces:
            (x, y, w, h) = face
            # Crop out the face image
            croppedFace = grayFrame[y:y + h, x:x + w]
            croppedFace = cv2.equalizeHist(croppedFace)
            # Resize for the recognition
            croppedFace = cv2.resize(croppedFace, (settings['resize_for_training'], settings['resize_for_training']))
            # Predict the person
            predictedLabel, predictedConfidence = model.predict(croppedFace)
            # Associate the number with a name
            personName = people[predictedLabel]

            # Draw a bounding box around the face (if already detected than green , if not detected than blue)
            if personName in accurate_predictions:
                cv2.rectangle(debugFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                cv2.rectangle(debugFrame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # We set a confidance threshold
            if predictedConfidence < settings['minConfidanceForPrediction']:
                # Check for "real" detections
                predictions.append(personName)
                if len(predictions) >= accuracy_number:
                    # Get the last X detections
                    predictions = predictions[-accuracy_number:]
                    # See how many elements are in the set (if 1 then the last X detections are the same)
                    s = set(predictions)
                    if len(s) == 1:
                        # Get the name of the person
                        person = list(s)[0]
                        if (person in accurate_predictions) is False:
                            print "Person added: " + person
                            # Add to the list
                            accurate_predictions.add(list(s)[0])

                            # Create a dictionary where the students name is the key and the arrival time is the value
                            arrivalTime = time.asctime(time.localtime(time.time()))
                            attendance_sheet_dict[person] = arrivalTime
                            print "\a\a"

                text = "I am: {0}; Conf: {1:.2f}".format(personName, predictedConfidence)
                cv2.putText(debugFrame, text, (x - 20, y - 5), cv2.FONT_HERSHEY_PLAIN, 1.1, (0, 0, 225), 1)

        # Display the resulting frame
        cv2.imshow('Press q to quit!', debugFrame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Create a pandas frame what we can save to an excel file
attendanceSheet = pd.DataFrame(attendance_sheet_dict.items(), columns=['Name', "Time"])
# Needed to install xlsxwriter!!!!
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('attendance_sheet' + str(datetime.datetime.now().date()) + '.xlsx', engine='xlsxwriter')
attendanceSheet.to_excel(writer, sheet_name='Attendance')
writer.save()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
