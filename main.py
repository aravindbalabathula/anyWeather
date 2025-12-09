from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime

app = Flask(__name__)

# OpenWeatherMap API (Free tier - sign up at openweathermap.org)
API_KEY = "b032dbdf3f22880a6a8716e40277ff12"  # Replace with your actual API key
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"

# Indian states with their capital cities
INDIAN_STATES = {
    "Andhra Pradesh": {"city": "Amaravati", "lat": 16.5062, "lon": 80.6480},
    "Arunachal Pradesh": {"city": "Itanagar", "lat": 27.0844, "lon": 93.6053},
    "Assam": {"city": "Dispur", "lat": 26.1433, "lon": 91.7898},
    "Bihar": {"city": "Patna", "lat": 25.5941, "lon": 85.1376},
    "Chhattisgarh": {"city": "Raipur", "lat": 21.2514, "lon": 81.6296},
    "Goa": {"city": "Panaji", "lat": 15.4909, "lon": 73.8278},
    "Gujarat": {"city": "Gandhinagar", "lat": 23.2156, "lon": 72.6369},
    "Haryana": {"city": "Chandigarh", "lat": 30.7333, "lon": 76.7794},
    "Himachal Pradesh": {"city": "Shimla", "lat": 31.1048, "lon": 77.1734},
    "Jharkhand": {"city": "Ranchi", "lat": 23.3441, "lon": 85.3096},
    "Karnataka": {"city": "Bengaluru", "lat": 12.9716, "lon": 77.5946},
    "Kerala": {"city": "Thiruvananthapuram", "lat": 8.5241, "lon": 76.9366},
    "Madhya Pradesh": {"city": "Bhopal", "lat": 23.2599, "lon": 77.4126},
    "Maharashtra": {"city": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    "Manipur": {"city": "Imphal", "lat": 24.8170, "lon": 93.9368},
    "Meghalaya": {"city": "Shillong", "lat": 25.5788, "lon": 91.8933},
    "Mizoram": {"city": "Aizawl", "lat": 23.7271, "lon": 92.7176},
    "Nagaland": {"city": "Kohima", "lat": 25.6747, "lon": 94.1086},
    "Odisha": {"city": "Bhubaneswar", "lat": 20.2961, "lon": 85.8245},
    "Punjab": {"city": "Chandigarh", "lat": 30.7333, "lon": 76.7794},
    "Rajasthan": {"city": "Jaipur", "lat": 26.9124, "lon": 75.7873},
    "Sikkim": {"city": "Gangtok", "lat": 27.3389, "lon": 88.6065},
    "Tamil Nadu": {"city": "Chennai", "lat": 13.0827, "lon": 80.2707},
    "Telangana": {"city": "Hyderabad", "lat": 17.3850, "lon": 78.4867},
    "Tripura": {"city": "Agartala", "lat": 23.8315, "lon": 91.2868},
    "Uttar Pradesh": {"city": "Lucknow", "lat": 26.8467, "lon": 80.9462},
    "Uttarakhand": {"city": "Dehradun", "lat": 30.3165, "lon": 78.0322},
    "West Bengal": {"city": "Kolkata", "lat": 22.5726, "lon": 88.3639},
    "Andaman and Nicobar Islands": {"city": "Port Blair", "lat": 11.6234, "lon": 92.7265},
    "Chandigarh": {"city": "Chandigarh", "lat": 30.7333, "lon": 76.7794},
    "Dadra and Nagar Haveli and Daman and Diu": {"city": "Daman", "lat": 20.4283, "lon": 72.8397},
    "Delhi": {"city": "New Delhi", "lat": 28.6139, "lon": 77.2090},
    "Jammu and Kashmir": {"city": "Srinagar", "lat": 34.0837, "lon": 74.7973},
    "Ladakh": {"city": "Leh", "lat": 34.1526, "lon": 77.5771},
    "Lakshadweep": {"city": "Kavaratti", "lat": 10.5626, "lon": 72.6369},
    "Puducherry": {"city": "Puducherry", "lat": 11.9416, "lon": 79.8083}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/states', methods=['GET'])
def get_states():
    """Return list of Indian states"""
    return jsonify({"states": sorted(INDIAN_STATES.keys())})

@app.route('/api/weather', methods=['POST'])
def get_weather():
    """Fetch weather data for selected state using coordinates"""
    try:
        data = request.get_json()
        state = data.get('state')
        
        if not state or state not in INDIAN_STATES:
            return jsonify({"error": "Invalid state selected"}), 400
        
        state_info = INDIAN_STATES[state]
        city = state_info["city"]
        lat = state_info["lat"]
        lon = state_info["lon"]
        
        # Make API request using coordinates
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": "metric"
        }
        
        response = requests.get(WEATHER_URL, params=params)
        
        if response.status_code == 200:
            weather_data = response.json()
            
            # Extract relevant information
            result = {
                "state": state,
                "city": city,
                "temperature": round(weather_data["main"]["temp"]),
                "feels_like": round(weather_data["main"]["feels_like"]),
                "humidity": weather_data["main"]["humidity"],
                "pressure": weather_data["main"]["pressure"],
                "description": weather_data["weather"][0]["description"].title(),
                "main": weather_data["weather"][0]["main"],
                "icon": weather_data["weather"][0]["icon"],
                "wind_speed": round(weather_data["wind"]["speed"] * 3.6, 1),
                "visibility": weather_data.get("visibility", 0) / 1000,
                "timestamp": datetime.now().strftime("%I:%M %p, %d %B %Y")
            }
            
            return jsonify(result)
        elif response.status_code == 401:
            return jsonify({"error": "Invalid API key. Please check your OpenWeatherMap API key."}), 401
        else:
            return jsonify({"error": f"Failed to fetch weather data: {response.status_code}"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


import os
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)