from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import requests
import random
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
CORS(app)

# Load models once at startup
with open('model_pkl', 'rb') as file:
    model = pickle.load(file)

with open('panel_model', 'rb') as file2:
    model2 = pickle.load(file2)

# Hugging Face API details
HUGGINGFACE_API_KEY = ''  # Replace with your Hugging Face API key
HUGGINGFACE_API_URL = 'https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-5'

algae_dict = {0: "Chlorella", 1: "Dunaliella", 2: "Haematococcus", 3: "Scenedesmus", 4: "Spirulina"}
panel_dict = {0: "Flat Panel", 1: "Tubular", 4: "Vertical Column", 5: "V-Shaped"}

def get_coordinates(location):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
    response = requests.get(geo_url)
    data = response.json()
    if not data.get("results"):
        return None, None
    result = data["results"][0]
    return result["latitude"], result["longitude"]

def get_weather_data(lat, lon):
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,relative_humidity_2m"
        f"&daily=precipitation_sum,sunshine_duration"
        f"&timezone=auto"
    )
    response = requests.get(weather_url)
    data = response.json()

    hourly = data.get("hourly", {})
    temperatures = hourly.get("temperature_2m", [])
    humidities = hourly.get("relative_humidity_2m", [])

    temperature = temperatures[-1] if temperatures else None
    humidity = humidities[-1] if humidities else None

    daily = data.get("daily", {})
    rainfall = daily.get("precipitation_sum", [None])[0]
    sunlight_hours = daily.get("sunshine_duration", [None])[0]

    return {
        "temperature": temperature,
        "humidity": humidity,
        "rainfall": rainfall,
        "sunlight_hours": sunlight_hours / 3600 if sunlight_hours else 0
    }

def simulate_water_quality(location):
    return {
        "ph": round(random.uniform(5, 8.5), 5),
        "nitrogen": round(random.uniform(0, 20), 5),
        "phosphorus": round(random.uniform(0, 5), 5),
        "bod": round(random.uniform(1, 100), 5)
    }

# Updated image generation function using Hugging Face API
def generate_image(algae_type, panel_type, algae_amount, wall_area):
    prompt = f"An illustration of a build's outside wall with algae type {algae_type} grown on a {panel_type} panel. " \
             f"Algae Amount {algae_amount} and Wall Area {wall_area}"

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "inputs": prompt
    }

    # Make the API request to generate the image
    response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=data)
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.text)
    
    if response.status_code != 200:
        return None

    # Get the generated image (base64 encoded) from the response
    image_base64 = response.json()[0]['generated_image']

    return image_base64

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    location = data.get("location")
    algae_amount = data.get("algae_amount")
    wall_area = data.get("wall_area")

    lat, lon = get_coordinates(location)
    if lat is None or lon is None:
        return jsonify({"error": "Location not found"}), 400

    weather = get_weather_data(lat, lon)
    water_quality = simulate_water_quality(location)

    features = [
        weather["temperature"],
        weather["humidity"],
        weather["sunlight_hours"],
        weather["rainfall"],
        water_quality["ph"],
        water_quality["nitrogen"],
        water_quality["phosphorus"],
        water_quality["bod"]
    ]

    algae_pred = model.predict([features])[0]
    algae_type = algae_dict[algae_pred]

    panel_pred = model2.predict([[algae_amount, wall_area, weather["temperature"], weather["sunlight_hours"], algae_pred]])[0]
    panel_type = panel_dict[panel_pred]

    # Generate image based on the prediction using Hugging Face API
    image_base64 = generate_image(algae_type, panel_type, algae_amount, wall_area)

    response = {
        'algae_type': algae_type,
        'panel_type': panel_type,
        'weather': weather,
        'water_quality': water_quality,
        'image': f"data:image/png;base64,{image_base64}"  # Embed the base64 image in a data URL
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
