import cv2
import pytesseract
import numpy as np

# Set up the webcam
cap = cv2.VideoCapture(0)

# Set up pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Loop through each frame from the webcam
i = 1
lower_green = np.array([0, 25, 25])
upper_green = np.array([255, 255, 255])
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    
    # Gaussian blur
    frame = cv2.GaussianBlur(frame,(5,5),0)
    
    # Convert the frame to grayscale
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply a threshold to the grayscale image
    #thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Mask out any colors that are not in the green color range
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Apply a threshold to the masked image
    thresh = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    
    # Apply some morphological transformations to the thresholded image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    if i%10==0:
        # Use pytesseract to recognize text in the image
        text = pytesseract.image_to_string(morph, config="--psm 8 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz")
        # config="-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz"
    
        # Print the recognized text to the command line
        print(text)
    i = i + 1
    
    # Show the original image with text overlay
    cv2.imshow("Original", frame)
    cv2.imshow("HSV", hsv)
    cv2.imshow("Text Detection", morph)
    
    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()


# import numpy as np
# import cv2 as cv
# cap = cv.VideoCapture(1)
# if not cap.isOpened():
#     print("Cannot open camera")
#     exit()
# while True:
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     # if frame is read correctly ret is True
#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break
#     # Our operations on the frame come here
#     gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#     # Display the resulting frame
#     cv.imshow('frame', gray)
#     if cv.waitKey(1) == ord('q'):
#         break
# # When everything done, release the capture
# cap.release()
# cv.destroyAllWindows()
