import cv2
from flask import Flask, render_template, request

app = Flask(__name__)
numbers = []
def read_number_from_image(image_path):
    image = cv2.imread(image_path)
    # Do some OpenCV processing to read the number from the image
    # ...
    numbers.append(1234)  # Replace this with the actual number you read from the image
    return numbers

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

