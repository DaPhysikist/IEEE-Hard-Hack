from flask import Flask, render_template

app = Flask(__name__)

@app.route('/data')
def display_data():
    # Retrieve data from server
    data = get_data_from_server()

    # Format data as needed
    formatted_data = format_data(data)

    # Render template with formatted data
    return render_template('data.html', data=formatted_data)
