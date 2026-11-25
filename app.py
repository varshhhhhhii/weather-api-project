from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Weather API Project is Running!"

@app.route("/weather")
def weather():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "Please enter a city name"}), 400

    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        return jsonify({
            "city": city,
            "temperature": data["current_condition"][0]["temp_C"],
            "weather": data["current_condition"][0]["weatherDesc"][0]["value"]
        })

    except requests.RequestException:
        return jsonify({"error": "Unable to fetch weather data"}), 502

    except (KeyError, IndexError, ValueError):
        return jsonify({"error": "Invalid weather data"}), 502

if __name__ == "__main__":
    app.run(debug=True)
