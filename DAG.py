## Job Scheduling

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

def my_python_function(**kwargs):
    print("Hello, Airflow!")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
}

with DAG(dag_id='run_incremental_updates', default_args=default_args, schedule_interval='@daily') as dag:
    run_external_script = BashOperator(
        task_id='reddit_to_sql',
        bash_command="/Users/brian.canyon/Documents/incremental_reddit_update.py"
    )
