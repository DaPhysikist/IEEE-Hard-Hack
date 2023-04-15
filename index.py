import cv2
from flask import Flask, render_template, request

app = Flask(__name__)
import cv2
import pytesseract

def read_number_from_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Preprocess the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(blurred, 100, 200)

    # Detect text regions using SWT
    swt = cv2.ximgproc.createStructuredEdgeDetection('model.yml')
    swt_edges = cv2.ximgproc.StructuredEdgeDetection_computeEdges(swt, edges)
    regions = cv2.ximgproc.createFastLineDetector().detect(swt_edges)

    # Extract characters using MSER
    mser = cv2.MSER_create()
    for region in regions:
        x, y, w, h = cv2.boundingRect(region)
        if w > h and w/h > 1.5:
            character = gray[y:y+h, x:x+w]
            _, character = cv2.threshold(character, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            cv2.imshow('Character', character)
            cv2.waitKey(0)
            text = pytesseract.image_to_string(character, config='--psm 10')
            try:
                number = int(text)
                return number
            except ValueError:
                pass


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Handle file upload and extract number from image
        image = request.files['file']
        number = read_number_from_image(image)
        return render_template('result.html', number=number)
    else:
        return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

