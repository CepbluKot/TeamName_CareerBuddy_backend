import os
from pathlib import Path
from airflow import DAG
from datetime import datetime, timedelta
from airflow.models import Variable
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from dotenv import load_dotenv


load_dotenv()

env_vars_general = {
    "AIRFLOW_UID": os.getenv("AIRFLOW_UID")
}

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 10, 1),
    "execution_timeout": timedelta(minutes=60),
}

CRON_SCHEDULE_CHANNEL_DATA_UPDATE = os.getenv("CRON_SCHEDULE_CHANNEL_DATA_UPDATE")
if not CRON_SCHEDULE_CHANNEL_DATA_UPDATE:
    CRON_SCHEDULE_CHANNEL_DATA_UPDATE = '1-59/20 * * * *'

dag = DAG(
    dag_id="ml_model",
    default_args=default_args,
    schedule_interval=CRON_SCHEDULE_CHANNEL_DATA_UPDATE,
    max_active_runs=1,
    # is_paused_upon_creation=False
)

kafka_clusters_cmdb_test = DockerOperator(
    dag=dag,
    task_id="ml_model_task",
    image="ml_model:latest",
    command="python3 ./ml_model.py",

    docker_url="unix://var/run/docker.sock",
    network_mode="host",
    environment=env_vars_general
)