from PIL import Image
from io import BytesIO
import redis
import base64
import json

# Connect to the Redis server
r = redis.Redis(
    host='redis-19450.c251.east-us-mz.azure.cloud.redislabs.com',
    port=19450,
    password='MyLoveForYouNeverCeasesToExist'
)

# Retrieve the image data from Redis
combined_data = r.get('Record9')

# Parse the JSON data to extract image data
image_and_prediction = json.loads(combined_data)

# Decode the Base64-encoded image data
image_data_base64 = image_and_prediction['image_data']
image_data = base64.b64decode(image_data_base64)

# Create a Pillow image from the binary data
image = Image.open(BytesIO(image_data))

# Display the image (for example, using Pillow's built-in viewer)
image.show()