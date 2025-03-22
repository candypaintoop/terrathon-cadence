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
    # Requesting both hourly and daily data
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,relative_humidity_2m"
        f"&daily=precipitation_sum,sunshine_duration"
        f"&timezone=auto"
    )

    response = requests.get(weather_url)
    data = response.json()

    # Extract hourly temperature & humidity
    hourly = data.get("hourly", {})
    temperatures = hourly.get("temperature_2m", [])
    humidities = hourly.get("relative_humidity_2m", [])

    # Get the latest value (you can change to average if needed)
    temperature = temperatures[-1] if temperatures else None
    humidity = humidities[-1] if humidities else None

    # Extract daily rainfall & sunshine hours (first value for today)
    daily = data.get("daily", {})
    rainfall = daily.get("precipitation_sum", [None])[0]
    sunlight_hours = daily.get("sunshine_duration", [None])[0]

    return {
        "temperature": temperature,
        "humidity": humidity,
        "rainfall": rainfall,
        "sunlight_hours": sunlight_hours/3600
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
location = "Bangalore"
result = get_combined_data(location)


with open('model_pkl', 'rb') as file:
    model = pickle.load(file)


predictions = model.predict([[result["weather"]["temperature"],result["weather"]["humidity"],result["weather"]["sunlight_hours"],result["weather"]["rainfall"],result["water_quality"]["ph"],result["water_quality"]["nitrogen"],result["water_quality"]["phosphorus"],result["water_quality"]["bod"]]])[0]

algae_dict = {0:"Chlorella",1:"Dunaliella",2:"Haematococcus",3:"Scenedesmus",4:"Spirulina"}
panel_dict = {0:"Flat Panel",1:"Tubular",4:"Vertical Column",5:"V-Shaped"}

with open('panel_model','rb') as file2:
    model2 = pickle.load(file2)

algae_amount = round(random.uniform(1,100),5)
wall_size = round(random.uniform(10,100),5)
predictions2 = model2.predict([[algae_amount,wall_size,result["weather"]["temperature"],result["weather"]["sunlight_hours"],predictions]])[0]
print(algae_dict[predictions],panel_dict[predictions2])
