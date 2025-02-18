import json
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.table import EnvironmentSettings, StreamTableEnvironment, Row
from dotenv import load_dotenv
import os

load_dotenv()

superset_db = os.getenv("POSTGRES_DB_SUPERSET")
db_user = os.getenv("POSTGRES_USER")
db_pass = os.getenv("POSTGRES_PASSWORD")

# Create the execution environment.
env = StreamExecutionEnvironment.get_execution_environment()

# Configure KafkaSource for your flight data.
kafka_source = KafkaSource.builder() \
    .set_bootstrap_servers("kafka:9093") \
    .set_topics("flight_data") \
    .set_group_id("groupId-919292") \
    .set_value_only_deserializer(SimpleStringSchema()) \
    .build()

# Create a DataStream from Kafka.
ds = env.from_source(
    kafka_source,
    WatermarkStrategy.no_watermarks(),
    "Kafka Source"
)

# Convert each JSON record into a Python dict, then map to a Row with flight-related fields.
flight_stream = ds.map(lambda s: json.loads(s)) \
    .map(lambda p: Row(
            flight_number=p["flight_number"],
            departure_airport=p["departure_airport"],
            arrival_airport=p["arrival_airport"],
            status=p["status"],
            airline=p["airline"],
            timestamp=p["timestamp"]),
         output_type=Types.ROW_NAMED(
            ["flight_number", "departure_airport", "arrival_airport", "status", "airline", "timestamp"],
            [Types.STRING(), Types.STRING(), Types.STRING(), Types.STRING(), Types.STRING(), Types.STRING()]
         )
)

# Create a StreamTableEnvironment.
settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
t_env = StreamTableEnvironment.create(env, environment_settings=settings)

# Convert the DataStream to a Table.
flights_table = t_env.from_data_stream(flight_stream)

jdbc_url = f"jdbc:postgresql://postgres:5432/{superset_db}"

# Define a Postgres sink table using DDL.
ddl = f"""
CREATE TABLE flights (
    flight_number STRING,
    departure_airport STRING,
    arrival_airport STRING,
    status STRING,
    airline STRING,
    `timestamp` STRING
) WITH (
    'connector' = 'jdbc',
    'url' = '{jdbc_url}',
    'table-name' = 'flights',
    'username' = '{db_user}',
    'password' = '{db_pass}'
)
"""

t_env.execute_sql(ddl)

# Insert the flight records into Postgres.
flights_table.execute_insert("flights").wait()
env.execute("Kafka2Postgres")
