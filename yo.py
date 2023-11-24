import requests

# URL of the server or API where you want to send the image
url = "https://annaninstance-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/c8ec3811-7c9e-4576-a8b9-232eef909efe/classify/iterations/ChestCancerPrediction/image"

# Path to the image file you want to send
image_path = "C:\\Users\\annan\\Downloads\\archive\\Data\\valid\\squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa\\000114 (6).png"


# Open and read the image file
with open(image_path, 'rb') as image_file:


    # Define the headers, if needed (e.g., content type)
    headers = {
        'Prediction-Key': "b84a761e1dc24029a24e6e46b878024a",
        'Content-Type': "application/octet-stream"
    }

    # Send a POST request with the image data as the request body
    response = requests.post(url, data=image_file, headers=headers)

# Check the response from the server
if response.status_code == 200:
    print("Image uploaded successfully.")
else:
    print(f"Error: {response.status_code}")
    print(response.text)  # Print the response content for debugging
