# Use the official Apache Airflow image
FROM apache/airflow:2.10.5-python3.10

# Set environment variables
ENV AIRFLOW_HOME=/opt/airflow
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
ENV PATH=$JAVA_HOME/bin:$PATH

# Install Java and dependencies as root
USER root
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk-headless procps && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Switch to airflow user for PySpark installation
USER airflow
RUN pip install --no-cache-dir pyspark
