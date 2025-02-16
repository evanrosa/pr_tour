from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg

spark = SparkSession.builder.appName("flight_analysis").getOrCreate()

df = spark.read.csv("/opt/airflow/data/flights/data.csv", header=True, inferSchema=True)

df_filtered = df.select("FlightDate", "Reporting_Airline", "Origin", "Dest", "DepDelay") \
    .filter(col("Dest") == "SJU")

avg_delays = df_filtered.groupBy("Reporting_Airline").agg(avg("DepDelay").alias("avg_delay"))

avg_delays.show()

avg_delays.write.mode("overwrite").parquet("data/processed/avg_delays")