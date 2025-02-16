import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB_SUPERSET")


print("POSTGRES_USER:", db_user)
print("POSTGRES_PASSWORD:", db_password)
print("POSTGRES_DB_SUPERSET:", db_name)


spark = SparkSession.builder \
    .appName("flight_analysis") \
    .config("spark.jars", "/opt/bitnami/spark/jars/postgresql-42.2.23.jar") \
    .getOrCreate()

df = spark.read.csv("/opt/airflow/data/flights/data.csv", header=True, inferSchema=True)

df_filtered = df.select("FlightDate", "Reporting_Airline", "Origin", "Dest", "DepDelay") \
    .filter(col("Dest") == "SJU")

avg_delays = df_filtered.groupBy("Reporting_Airline").agg(avg("DepDelay").alias("avg_delay"))

avg_delays.show()

# Write the results to PostgreSQL using JDBC
jdbc_url = f"jdbc:postgresql://postgres:5432/{db_name}"
table_name = "public.avg_delays"
connection_properties = {
    "user": db_user,
    "password": db_password,
    "driver": "org.postgresql.Driver"
}

avg_delays.write \
    .mode("overwrite") \
    .jdbc(url=jdbc_url, table=table_name, properties=connection_properties)