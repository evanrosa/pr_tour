# Use Apache Flink as the base image
FROM apache/flink:1.20.0

# Set working directory
WORKDIR /opt/flink

# Install Python and PyFlink dependencies
RUN apt-get update && apt-get install -y python3 python3-pip python3-dev && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# COPY only requirements.txt first (prevents rebuilding everything if code changes)
COPY ../../requirements.txt /opt/flink/job/

# 🔥 Install dependencies before copying the rest of the files
RUN pip3 install --no-cache-dir --prefer-binary --disable-pip-version-check --timeout=100 -r /opt/flink/job/requirements.txt

RUN rm -rf /scripts/jars

# Copy actual script files after dependencies (ensures Docker caching efficiency)
COPY ../../scripts/flink_processor.py /opt/flink/job/
COPY ../../dags/config/flink-conf.yaml /opt/flink/conf/flink-conf.yaml

# Copy your connector and dependency jars
COPY ../../dags/jars/flink-connector-kafka-3.4.0-1.20.jar /opt/flink/lib/
COPY ../../dags/jars/kafka-clients-3.4.0.jar /opt/flink/lib/
COPY ../../dags/jars/flink-python-1.20.0.jar /opt/flink/lib/
COPY ../../dags/jars/flink-connector-jdbc-core-3.3-SNAPSHOT.jar /opt/flink/lib/
COPY ../../dags/jars/flink-connector-jdbc-postgres-3.3-SNAPSHOT.jar /opt/flink/lib/
COPY ../../dags/jars/postgresql-42.2.23.jar /opt/flink/lib/


# ✅ Ensure Flink recognizes the Python JAR
ENV FLINK_CLASSPATH="/opt/flink/lib/flink-python-1.20.0.jar"

# Set Python environment for Flink
ENV PYTHONPATH="/opt/flink/job"
ENV FLINK_PYTHON_EXECUTABLE="/usr/bin/python3"

# Expose required ports for Flink UI and RPC communication
EXPOSE 8081 6123 6124

# Start Flink cluster on container startup
CMD ["start-cluster.sh"]
