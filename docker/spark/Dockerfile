# Use the Bitnami Spark image as base
FROM bitnami/spark:latest

# (Optional) Set a working directory (not strictly needed here)
WORKDIR /opt/bitnami/spark

# Copy the PostgreSQL JDBC jar from your host into the container.
# Adjust the source path as needed.
COPY ./dags/jars/postgresql-42.2.23.jar /opt/bitnami/spark/jars/

# Optionally, if you have custom Spark configuration, copy it too:
# COPY ./docker/spark/spark-defaults.conf /opt/bitnami/spark/conf/spark-defaults.conf

# (You might not need an explicit CMD if you rely on the Bitnami image’s entrypoint.)
