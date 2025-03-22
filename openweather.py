import requests

def get_city_data(api_key, city):
    url = f"https://api.airvisual.com/v2/city?city={city}&state=state_name&country=country_name&key={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def main():
    API_KEY = "94de9399-2f11-4a2a-a63f-997309416337"
    
    # Get city input from user
    city = input("Please enter a city name: ")
    
    print(f"Fetching weather data for {city}...")
    data = get_city_data(API_KEY, city)
    
    if data and data.get("status") == "success":
        current = data.get("data", {}).get("current", {})
        weather = current.get("weather", {})
        
        # Note: Standard IQAir API doesn't typically provide pH, rainfall, or exact sunlight hours
        # You would need to either use a different API or calculate these values
        
        # Display available data
        print(f"\nWeather data for {city}:")
        print(f"Temperature: {weather.get('tp', 'N/A')}°C")
        print(f"Humidity: {weather.get('hu', 'N/A')}%")
        print(f"Wind Speed: {weather.get('ws', 'N/A')} m/s")
        
        # If you had access to these data points, you would display them like this:
        print(f"pH level: N/A (Not available in standard IQAir API)")
        print(f"Rainfall: N/A (Not available in standard IQAir API)")
        print(f"Sunlight hours: N/A (Not available in standard IQAir API)")
        
        # You might want to supplement with data from another API
        print("\nNote: For pH, rainfall, and sunlight hours data, you may need to use an additional weather API.")
    else:
        print(f"Failed to retrieve data for {city}")

if __name__ == "__main__":
    main()