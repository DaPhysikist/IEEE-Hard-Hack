from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Handle file upload and extract number from image
        image = request.files['file']
        number = read_number_from_image(image)
        return render_template('result.html', number=number)
    else:
        return render_template('data.html')

if __name__ == '__main__':
    app.run(debug=True)
