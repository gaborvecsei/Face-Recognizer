"""
/*****************************************************
 *
 *              Gabor Vecsei
 * Email:       vecseigabor.x@gmail.com
 * Blog:        https://gaborvecsei.wordpress.com/
 * LinkedIn:    www.linkedin.com/in/vecsei-gabor
 * Github:      https://github.com/gaborvecsei
 *
 *****************************************************
 """

import os
import sys


def cls():
    """
    # Clears the console's screen
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def mainMenu():
    """
    # Goes to the main menu if the user presses x
    """
    print 'Press (x) to go back to the main menu'
    pressedKey = raw_input('')
    if pressedKey == 'x' or pressedKey == 'X':
        cls()
        mainScreen()
    else:
        mainMenu()


def mainScreen():
    """
    # Shows main screen where we can choose from the programs
    """
    print "\n\nFace Recognizer --- Gabor Vecsei"
    print "---------------------------------------------------------"
    print "Press 1 to prepare images for training (from folder)"
    print "Press 2 to prepare images for training (from webcam)"
    print "Press 3 to train face recognizer"
    print "Press 4 to reconize face from webcam image"
    print "Press 5 to recognize face and create attendance sheet"
    print "Press 6 for About"
    print "Press 7 to exit"
    print "---------------------------------------------------------\n\n"
    selectedMenuPoint = raw_input("Enter the selected menu point and press ENTER: ")
    print "\n\n"

    # Start the chosen script
    screenDict[eval(selectedMenuPoint)]()


# These are the menu options we can execute
# We run a .py script

def prepImagesFromFolder():
    cls()
    os.system("python prepare_faces_for_training.py")
    mainMenu()


def prepImagesFromWebcam():
    cls()
    os.system("python prepare_faces_for_training_from_webcam.py")
    answer = raw_input("Would you like to add another person? (y/n)")
    if answer == 'y':
        prepImagesFromWebcam()
    mainMenu()


def trainFaceRecognizer():
    cls()
    os.system("python train_face_recognizer.py")
    mainMenu()


def recognizeFromWebcam():
    cls()
    os.system("python recognize_face_on_camera.py")
    mainMenu()


def recognizeFromWebcamAndCreateAttendanceSheet():
    cls()
    os.system("python recognize_face_create_attendance_sheet.py")
    mainMenu()


def exit():
    sys.exit(0)


def aboutScreen():
    cls()
    print "		Facial recognition system made by Gabor Vecsei"
    print "		BME BSc Thesis"
    print "		2016 December"
    print """
		/*****************************************************
		*
		*              Gabor Vecsei
		* Email:       vecseigabor.x@gmail.com
		* Blog:        https://gaborvecsei.wordpress.com/
		* LinkedIn:    www.linkedin.com/in/vecsei-gabor
		* Github:      https://github.com/gaborvecsei
		*
		*****************************************************
		"""
    mainMenu()

screenDict = {
    1: prepImagesFromFolder,
    2: prepImagesFromWebcam,
    3: trainFaceRecognizer,
    4: recognizeFromWebcam,
    5: recognizeFromWebcamAndCreateAttendanceSheet,
    6: aboutScreen,
    7: exit
}

# Program starts here:
mainScreen()