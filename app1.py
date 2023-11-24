import logging
from flask import Flask, request, render_template, jsonify
from flask_restx import Api, Resource
import requests
import json
import redis
import base64
from flask_cors import CORS

app = Flask(__name__)
api = Api(app, version='1.0.0', title='Classification', description='API for image classification using Azure Custom Vision')
CORS(app)

# Configure the logging
logging.basicConfig(filename='custom_vision_errors.log', level=logging.ERROR)

# Define your Azure Custom Vision API endpoint and prediction key here
custom_vision_endpoint = 'https://annaninstance-prediction.cognitiveservices.azure.com'
custom_vision_api_key = 'b84a761e1dc24029a24e6e46b878024a'

# Connect to the Redis server
r = redis.StrictRedis(
    host='redis-19450.c251.east-us-mz.azure.cloud.redislabs.com',
    port=19450,
    password='MyLoveForYouNeverCeasesToExist'
)

# Initialize the record counter from Redis, or set it to 1 if not found
record_counter = int(r.get('record_counter') or 1)

@api.route('/')
class Index(Resource):
    def get(self):
        return render_template('index.html')

@api.route('/upload')
class Upload(Resource):
    @api.response(200, 'Successful classification')
    @api.expect(api.parser().add_argument('image', type='file', location='files'))
    def post(self):
        global record_counter  # Access the counter variable
        try:
            # Handle the image upload
            uploaded_file = request.files['image']

            if not uploaded_file:
                return "No image provided.", 400

            image_data = uploaded_file.read()

            # Set up the Custom Vision API endpoint for image classification
            prediction_url = "https://annaninstance-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/c8ec3811-7c9e-4576-a8b9-232eef909efe/classify/iterations/ChestCancerPrediction/image"

            headers = {
                'Prediction-Key': custom_vision_api_key,
                'Content-Type': "application/octet-stream"
            }

            # Send the image to the Custom Vision API for classification
            response = requests.post(prediction_url, data=image_data, headers=headers)

            if response.status_code == 200:
                prediction_data = json.loads(response.text)

                # Use the record counter to generate the key
                unique_key = f'Record{record_counter}'

                # Increment the record counter for the next entry
                record_counter += 1

                # Store the updated record counter in Redis
                r.set('record_counter', record_counter)

                # Encode the binary image data to Base64
                image_data_base64 = base64.b64encode(image_data).decode('utf-8')

                # Combine Base64-encoded image and prediction data into a single JSON object
                image_and_prediction = {
                    'prediction_data': prediction_data,
                    'image_data': image_data_base64
                }

                # Store the combined data in Redis under the unique key
                r.set(unique_key, json.dumps(image_and_prediction))

                # Process the prediction results and display them in a template
                return render_template('result.html', prediction=prediction_data, unique_key=unique_key)
            else:
                error_message = f"Error {response.status_code}: {response.text}"
                logging.error(error_message)  # Log the error
                return "Error: Unable to classify the image.", 500
        except Exception as e:
            error_message = f"An exception occurred: {str(e)}"
            logging.error(error_message)  # Log the exception
            return "An unexpected error occurred.", 500

if __name__ == '__main__':
    app.run(debug=True)

