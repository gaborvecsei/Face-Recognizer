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

# Read the settings file
with open('settings_for_recognition.json') as settings_file:
    settings = json.load(settings_file)

# In the Input folder we store our "raw images about the people"
# In the output folder we will store the cropped images (those are automatically generated)
inputFolderPath = settings['input_folder']
outputFolderPath = settings['output_folder']

# If input folder does not exists than exit
if not os.path.exists(inputFolderPath) and os.path.isdir(inputFolderPath):
    print "Input folder does not exists: " + inputFolderPath
    sys.exit(1)

# Loading the face cascade
face_cascade = cv2.CascadeClassifier(settings['face_cascade_path'])

# Check all the sub-folders in the input folder
for subFolder in os.listdir(inputFolderPath):
    subFolderPath = os.path.join(inputFolderPath, subFolder)
    if os.path.isdir(subFolderPath):
        # Every subfolder represents a person (and the folder name is the person's name)
        personName = subFolder
        inputPath = os.path.join(inputFolderPath, personName)
        outputPath = os.path.join(outputFolderPath, personName)

        # If we don't have the output folder with the correct name, we have to make it
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)

        # Iterate thru all the images in the subfolder
        for imageName in os.listdir(inputPath):
            imageExtension = imageName.split('.')[-1]
            # Check if we use an actual image
            if imageExtension in ['jpg', 'png', 'jpeg', 'bmp']:
                # Get the image
                imageRGB = cv2.imread(inputPath + "/" + imageName)
                # Convert it to grayscale
                imageGray = cv2.cvtColor(imageRGB, cv2.COLOR_BGR2GRAY)
                # Detect faces
                faces = face_cascade.detectMultiScale(
                    imageGray,
                    scaleFactor=settings["scaleFactor"],
                    minNeighbors=settings["minNeighbors"],
                    minSize=(30, 30),
                    flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

                # If we have multiple faces on the images we have to save those too
                i = 0
                for face in faces:
                    i += 1
                    # Coordinates of the face
                    x, y, w, h = face
                    faceImage = imageRGB[y:y + h, x:x + w]
                    # Save the face to the output folder
                    fullImageName = outputPath + "/" + imageName + "_" + str(i) + ".jpg"
                    cv2.imwrite(fullImageName, faceImage)
                    print "Face detected and cropped: " + fullImageName

print "\nFace detection and preparation stopped."
print "Now you can train the face recognizer."
