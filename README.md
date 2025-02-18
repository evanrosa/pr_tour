# Real-Time Flight & Tourism Analysis (Puerto Rico)

## 📌 Project Overview
This project builds an **ETL pipeline** using **Kafka, Flink, Spark, and Airflow** to process real-time and historical flight data for **Puerto Rico (SJU Airport)**. The goal is to:

- **Stream real-time flight data** using Kafka.
- **Process streaming data** with Flink.
- **Analyze historical flight trends** using Spark.
- **Orchestrate workflows** using Airflow.
- **Store results** in PostgreSQL for visualization.

## 🏗 Tech Stack
- **Apache Kafka** → Stream real-time flight data
- **Apache Flink** → Process live streaming data
- **Apache Spark** → Perform batch analytics on historical data
- **Apache Airflow** → Orchestrate and schedule tasks
- **PostgreSQL** → Store processed data
- **Superset/Streamlit** → Dashboard for insights (optional)

## 📂 Project Structure
```
├── dags/                  # Airflow DAGs for scheduling
│   ├── flight_etl_dag.py  # Airflow DAG for orchestration
│   ├── spark_etl.py       # Spark job for batch processing
├── data/
│   ├── flights/           # Historical flight data (CSV)
│   ├── processed/         # Output of Spark jobs
├── scripts/
│   ├── kafka_producer.py  # Fetches real-time flight data
│   ├── flink_processor.py # Flink job for streaming analysis
├── docker-compose.yml     # Docker setup for Kafka, Spark, Flink, Airflow
├── README.md              # Project documentation
```

## 🚀 How to Run the Project
### 1️⃣ Start Kafka, Spark, Flink, and Airflow
```bash
docker compose up -d
```

### 2️⃣ Run the Kafka Producer (Real-Time Flight Data Fetcher)
```bash
docker compose run kafka_producer
```

### 3️⃣ Run the Flink Streaming Processor
```bash
Inside `docker` - flink run -py /opt/flink/job/flink_processor.py
```

### 4️⃣ Run the Spark Batch Processor
```bash
python scripts/spark_etl.py
```

### 5️⃣ Start Airflow Scheduler & Webserver
```bash
airflow scheduler & airflow webserver
```

### 6️⃣ Check DB Tables
```docker exec -it postgres psql -U evro -d pr_tour_superset
```

### You may need to create a user for airflow
```
docker exec -it airflow airflow db upgrade

docker exec -it airflow airflow users create \
  --username abc \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password xyz
```



## 📊 Data Sources
- **Real-Time Flights:** [AviationStack API](https://aviationstack.com/)
- **Historical Flight Data:** [FAA TranStats](https://www.transtats.bts.gov/)
- **Weather Data (Optional):** [NOAA/NWS API](https://www.weather.gov/documentation/services-web-api)
- **Puerto Rico Open Data:** [data.pr.gov](https://data.pr.gov/)


## flowchart LR
    ```subgraph Data_Sources[Data Sources]
        A[AviationStack API]
        B[Historical Flight Data (FAA)]
    end

    subgraph Streaming_Layer[Streaming Layer]
        A --> C[Kafka Producer]
        C --> D[Kafka Cluster]
        D --> E[Flink Streaming Job]
    end

    subgraph Batch_Layer[Batch Processing Layer]
        B --> F[Airflow DAG]
        F --> G[Spark ETL Job]
    end

    subgraph Storage[Data Storage]
        E --- H[Postgres Database]
        G --- H
    end

    subgraph Visualization[Visualization]
        H --> I[Superset Dashboard]
    end```


## 🎯 Future Enhancements
- ✅ Add real-time **dashboard** using Streamlit or Superset.
- ✅ Implement **machine learning** for flight delay predictions.
- ✅ Optimize Airflow DAGs for better scheduling.

## 🤝 Contributing
Feel free to fork, modify, and contribute to this project! 🚀

## 📜 License
This project is **open-source** under the MIT License.