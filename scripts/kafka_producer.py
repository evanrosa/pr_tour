import os
import requests
import json
from kafka import KafkaProducer
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_KEY")
KAFKA_TOPIC = "flight_data"

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)

def fetch_flights():
    url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&arr_iata=SJU"
    response = requests.get(url)
    #flights = response.json()["data"]

    flights = response.json().get("data", [])

    # Debug: Print the number of flights received
    print(f"Total flights received: {len(flights)}")

    if not flights:
        print("No flights found!")
        return



    for flight in flights:
        data = {
            "flight_number": flight["flight"]["iata"],
            "departure_airport": flight["departure"]["iata"],
            "arrival_airport": flight["arrival"]["iata"],
            "status": flight["flight_status"],
            "airline": flight["airline"]["name"],
            "timestamp": flight["departure"]["estimated"]
        }

        producer.send(KAFKA_TOPIC, value=data)
        print(f"Sent {data} to Kafka")
        # time.sleep(2)

    producer.flush()

if __name__ == "__main__":
    fetch_flights()

