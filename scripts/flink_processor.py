from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource
from pyflink.common.watermark_strategy import WatermarkStrategy
import json
import os

env = StreamExecutionEnvironment.get_execution_environment()

# 🔥 Explicitly Add JARs from the Correct Path `/opt/flink/lib/`
env.add_jars("file:///opt/flink/lib/flink-connector-kafka-3.4.0-1.20.jar")
env.add_jars("file:///opt/flink/lib/kafka-clients-3.9.0.jar")
env.add_jars("file:///opt/flink/lib/flink-python-1.20.0.jar")

kafka_source = KafkaSource.builder() \
    .set_bootstrap_servers("kafka:9093") \
    .set_topics("flight_data") \
    .set_value_only_deserializer(SimpleStringSchema()) \
    .build()

ds = env.from_source(
    kafka_source,
    watermark_strategy=WatermarkStrategy.no_watermarks(),
    source_name="Kafka Source"
)

# Convert the JSON string into a Python dictionary
ds = ds.map(lambda s: json.loads(s))

def process_flight(flight):
    if flight["status"] == "delayed":
        print(f"Flight {flight['flight_number']} is delayed")

ds.map(process_flight)
env.execute("Flight Data Processing")
