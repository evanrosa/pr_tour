import os
import requests
import json
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_KEY")
producer = KafkaProducer(
    bootstrap_servers="kafka:9093",
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)

def fetch_flights(topic_name, airport):
    url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&arr_iata={airport}"
    response = requests.get(url)
    print("Status code:", response.status_code)
    print("Response text:", response.text)

    flights = response.json().get("data", [])

    if not flights:
        print(f"No flights found! {flights.status_code}")
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

        producer.send(topic_name, value=data)
        print(f"Sent {data} to Kafka")
    producer.flush()

def fetch_future_flights(topic_name, date, airport):
    url = f"http://api.aviationstack.com/v1/flightsFuture?iataCode={airport}&type=arrival&date={date}&access_key={API_KEY}"
    response = requests.get(url)
    print("Status code:", response.status_code)
    print("Response text:", response.text)

    flights = response.json().get("data", [])

    print("flights", flights)

    if not flights:
        print(f"No flights found! {flights.status_code}")
        return

    for flight in flights:
        data = {
            "flight_number": flight["flight"]["iataNumber"],
            "departure_airport": flight["departure"]["iataCode"],
            "arrival_airport": flight["arrival"]["iataCode"],
            "airline": flight["codeshared"]["airline"]["name"],
            "departure": flight["departure"]["scheduledTime"],
            "arrival": flight["arrival"]["scheduledTime"]
        }

        producer.send(topic_name, value=data)
        print(f"Sent {data} to kafka")
    producer.flush()

if __name__ == "__main__":
    fetch_flights("flight_data", "SJU")
    fetch_future_flights("future_flights", "2025-02-18", "SJU")

