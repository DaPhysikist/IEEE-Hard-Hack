# import the necessary packages
import time
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import numpy as np
import pytesseract
import threading

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
STARTING_VALUE = "125"

class Camera(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.lcd_value = STARTING_VALUE

        # Set up the webcam
        self.cap = cv2.VideoCapture(0)

    def get_lcd_value(self):
        return self.lcd_value

    def run(self):
        while True:
            # Read a frame from the webcam
            frame = self.cap.read()

            # pre-process the image by resizing it, converting it to
            # graycale, blurring it, and computing an edge map
            image = imutils.resize(frame, height=500)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            edged = cv2.Canny(blurred, 50, 200, 255)

            # find contours in the edge map, then sort them by their
            # size in descending order
            cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
            displayCnt = None
            # loop over the contours
            for c in cnts:
                # approximate the contour
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                # if the contour has four vertices, then we have found
                # the thermostat display
                if len(approx) == 4:
                    displayCnt = approx
                    break
                
            # extract the thermostat display, apply a perspective transform
            # to it
            warped = four_point_transform(thresh, displayCnt.reshape(4, 2))

            # threshold the warped image, then apply a series of morphological
            # operations to cleanup the thresholded image
            thresh2 = cv2.threshold(warped, 0, 255,
                cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
            thresh2 = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
            height, width = thresh2.shape[:2]
            start_row = int(height * 0.30)
            start_col = int(width*0.30)
            end_row = int(height * 0.70)
            end_col = int(width * 0.70)
            kernel = np.ones((5, 5), np.uint8)
            #thresh2 = cv2.erode(thresh2, kernel, iterations=1)
            # cv2.dilate(thresh2, kernel, iterations=20)
            thresh2 = thresh2[start_row:end_row, start_col:end_col]

            gray = 255*(thresh2 < 128).astype(np.uint8) # To invert the text to white
            coords = cv2.findNonZero(gray) # Find all non-zero points (text)
            x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
            #thresh2 = thresh2[y-10:y+h+10, x-10:x+w+10] # Crop the image - note we do this on the original image

            imgchar = pytesseract.image_to_string(thresh2, config="--psm 13 -c tessedit_char_whitelist=0123456789.")
            self.lcd_value = imgchar