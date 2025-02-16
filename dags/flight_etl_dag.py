from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

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


run_spark_etl