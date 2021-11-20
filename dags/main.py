from datetime import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from get_data_instagram import get_data_instagram
from get_data_twitter import get_data_twitter
from preprocess_data import preprocess_data
from save_to_bigquery import save_to_bigquery

with DAG(
    dag_id="main_dag",
    start_date=datetime(2021, 10, 28),
    schedule_interval="@daily",
    is_paused_upon_creation=False,
    catchup=False,
) as main_dag:
    get_data_instagram_op = PythonOperator(
        task_id="get_data_instagram",
        provide_context=False,
        python_callable=get_data_instagram,
        dag=main_dag,
    )
    get_data_twitter_op = PythonOperator(
        task_id="get_data_twitter",
        provide_context=False,
        python_callable=get_data_twitter,
        dag=main_dag,
    )
    preprocess_data_op = PythonOperator(
        task_id="preprocess_data",
        provide_context=False,
        python_callable=preprocess_data,
        dag=main_dag,
    )
    save_to_bigquery_op = PythonOperator(
        task_id="save_to_bigquery",
        provide_context=False,
        python_callable=save_to_bigquery,
        dag=main_dag,
    )

    get_data_instagram_op >> get_data_twitter_op >> preprocess_data_op >> save_to_bigquery_op
