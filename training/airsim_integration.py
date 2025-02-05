import requests
import json

def fetch_airsim_data():
    url = "http://localhost:41451/api/simGetImages"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    print("AirSim integration: Data fetched", data)
    return data

if __name__ == "__main__":
    fetch_airsim_data()
