import logging
from flask import Flask, request, render_template
import requests
import json

app = Flask(__name__)

# Configure the logging
logging.basicConfig(filename='custom_vision_errors.log', level=logging.ERROR)

# Define your Azure Custom Vision API endpoint and prediction key here
custom_vision_endpoint = 'https://annaninstance-prediction.cognitiveservices.azure.com'
custom_vision_api_key = 'b84a761e1dc24029a24e6e46b878024a'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        # Handle the image upload
        uploaded_file = request.files['image']
        files = uploaded_file.read()
        #files = open(uploaded_file, 'rb')

        if not uploaded_file:
            return "No image provided."

        # Set up the Custom Vision API endpoint for image classification
        prediction_url = "https://annaninstance-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/c8ec3811-7c9e-4576-a8b9-232eef909efe/classify/iterations/ChestCancerPrediction/image"

        headers = {
            'Prediction-Key': "b84a761e1dc24029a24e6e46b878024a",
            'Content-Type': "application/octet-stream"
        }

        # Send the image to the Custom Vision API for classification
        #files = {'image': (uploaded_file.filename, uploaded_file.stream, uploaded_file.mimetype)}
        #files = {'image': (uploaded_file.filename, uploaded_file.read(), uploaded_file.mimetype)}

        response = requests.post(prediction_url, data=files, headers=headers )

        if response.status_code == 200:
            prediction_data = json.loads(response.text)
            # Process the prediction results and display them in a template
            return render_template('result.html', prediction=prediction_data)
        else:
            error_message = f"Error {response.status_code}: {response.text}"
            logging.error(error_message)  # Log the error
            return "Error: Unable to classify the image."
    except Exception as e:
        error_message = f"An exception occurred: {str(e)}"
        logging.error(error_message)  # Log the exception
        return "An unexpected error occurred."

if __name__ == '__main__':
    app.run(debug=True)