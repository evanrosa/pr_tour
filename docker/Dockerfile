FROM python:3.10

# Set working directory in the container
WORKDIR /app

# Install required packages
RUN pip install --no-cache-dir requests pyspark pyflink kafka-python python-dotenv

# Copy your scripts folder into the image
COPY ./scripts /app/scripts

# Set the default command to run your desired script
CMD ["python", "scripts/kafka_producer.py", "scripts/flink_processor.py"]