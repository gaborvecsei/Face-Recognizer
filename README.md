# Thesis

--------------------------------

# Face Recognizer

This is my Thesis at the University for the final BSc semester.

-------------------------------

## Setup

### Required

- **OpenCV** - 2.4.
- **Python** - 2.7.

Install OpenCV as you can see on the [offical site](http://opencv.org/).
Or you can use [Anaconda](https://anaconda.org/) enviroment for easy setup.

After the setup you should check *settings_for_recognition.json* because there you can see the global settings.

## Run it

1. Collect data and place it in *input_images* folder if you would like to prepare the data from that source. If you would like to use webcam than just skip this step.
2. Run `python face_recognizer_menu.py`
3. Choose from the menu points:
	- 1: Prepare the training data from the folder (*input_images*)
	- 2: Prepare training data from webcam (results will be saved to *output_images*)
	- 3: Train the face recognizer with the prepared data (model will be saved to *saved_model*)
	- 4: Test face recognition with a webcam
	- 5: Recognize from camera and create attendance sheet
	- 6: About
	- 7: Exit from the application

-------------------------------

## Folder Structure

```
cascades/
	hc_face.xml
input_images/
	Peter/
		peter1.jpg
		peter2.jpg
		...
	Dori/
		dori1.jpg
		dori2.jpg
		...
	Mona/
		mona1.jpg
		mona2.jpg
		...
	...
output_images/
	There are generated folders and images for the training
saved_models/
	Here you can saved the trained model
documentation/
	Face_Detection_And_Recognition_By_Gabor_Vecsei.pdf
```

-------------------------------

## About

Gábor Vecsei

[Personal Blog](https://gaborvecsei.wordpress.com/)

[Github](https://github.com/gaborvecsei)

[LinkedIn](https://www.linkedin.com/in/gaborvecsei)

Email: vecseigabor.x@gmail.com

2016.12.09.