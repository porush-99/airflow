import requests

from airflow.models import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime


def capture_api_response():
    response = requests.get('https://dummyjson.com/products/1')

    if response.status_code == 200:
        return response.json()['description']

    return 'no response'


with DAG("first_dag",
         start_date=datetime(2023, 12, 31),
         catchup=False,
         schedule_interval=None):

    start = EmptyOperator(
        task_id='start'
    )

    capture_response = PythonOperator(
        task_id='capture_response',
        python_callable=capture_api_response
    )

    end = EmptyOperator(
        task_id='end'
    )

    start >> capture_response >> end
