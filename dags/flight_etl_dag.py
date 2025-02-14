from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

from airflow.utils import retries

default_args = {
    "owner": "Evan Rosa",
    "start_date": datetime(2023, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "flight_etl_dag",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
)

run_spark_etl = BashOperator(
    task_id="run_spark_etl",
    bash_command="python /opt/airflow/dags/spark_etl.py",
    dag=dag,
)

run_flink_streaming = BashOperator(
    task_id="run_flink_streaming",
    bash_command="python /opt/airflow/scripts/flink_processor.py",
    dag=dag,
)

run_spark_etl >> run_flink_streaming