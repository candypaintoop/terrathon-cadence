import pickle
import requests
import random

def get_coordinates(location):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
    response = requests.get(geo_url)
    data = response.json()

    if not data.get("results"):
        return None, None

    result = data["results"][0]
    return result["latitude"], result["longitude"]

def get_weather_data(lat, lon):
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m,precipitation,sunshine_duration&timezone=auto"
    
    response = requests.get(weather_url)
    data = response.json()

    # Extract current/latest data from hourly arrays
    hourly = data.get("hourly", {})
    temperature = hourly.get("temperature_2m", [None])[-1]
    humidity = hourly.get("relative_humidity_2m", [None])[-1]
    rainfall = hourly.get("precipitation", [None])[-1]
    sunlight_hours = hourly.get("sunshine_duration", [None])[-1]

    return {
        "temperature": temperature,
        "humidity": humidity,
        "rainfall": rainfall,
        "sunlight_hours": sunlight_hours
    }

def simulate_water_quality(location):
    # Replace this with real data when available
    return {
        "ph": round(random.uniform(5, 8.5), 5),
        "nitrogen": round(random.uniform(0, 20), 5),
        "phosphorus": round(random.uniform(0, 5), 5),
        "bod": round(random.uniform(1, 100), 5)
    }

def get_combined_data(location):
    lat, lon = get_coordinates(location)
    
    if lat is None or lon is None:
        return {"error": "Location not found"}

    weather = get_weather_data(lat, lon)
    water_quality = simulate_water_quality(location)

    result = {
        "location": location,
        "latitude": lat,
        "longitude": lon,
        "weather": weather,
        "water_quality": water_quality
    }

    return result

# Example
location = "New York"
result = get_combined_data(location)


with open('model_pkl', 'rb') as file:
    model = pickle.load(file)


predictions = model.predict([[result["weather"]["temperature"],result["weather"]["humidity"],result["weather"]["sunlight_hours"],result["weather"]["rainfall"],result["water_quality"]["ph"],result["water_quality"]["nitrogen"],result["water_quality"]["phosphorus"],result["water_quality"]["bod"]]])
print(predictions)
