#DOES NOT WORK 4/15 8:24pm
import cv2
import pytesseract
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
font_scale = 1.5
font = cv2.FONT_HERSHEY_PLAIN

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    cap = cv2.VideoCapture(1)
if not cap.isOpened():
    raise IOError("Cannot open video")

cntr = 0
while True:
    ret, frame = cap.read()
    frame = cv2.GaussianBlur(frame,(25,25),0)
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply a threshold to the grayscale image
    frame = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cntr = cntr+1
    if cntr%20==0:
        imgH, imgW = frame.shape
        
        x1,y1,w1,h1 = 0,0,imgH,imgW
        
        imgchar = pytesseract.image_to_string(frame, config="-c tessedit_char_whitelist=.0123456789")
        
        imgboxes = pytesseract.image_to_boxes(frame)
        for boxes in imgboxes.splitlines():
            boxes = boxes.split(' ')
            x,y,w,h = int(boxes[1]),int(boxes[2]),int(boxes[3]),int(boxes[4])
            cv2.rectangle(frame, (x,imgH-y), (w,imgH-h), (0,0,255), 3)
        
        cv2.putText(frame,imgchar, (x1 + int(w1/50), y1 + int(h1/50)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        cv2.imshow('Text Detection', frame)
        print(imgchar)
        
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

