import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator

from myflow.tasks.twitter.module import FetchTwitter


# 設定DAG參數
default_args = {
    "owner": "johntung",
    "retries": 1,
    "retry_delay": pendulum.duration(minutes=1),
    "start_date": pendulum.datetime(2023, 9, 6),
}


with DAG(
    "fetch_twitter",
    default_args=default_args,
    schedule_interval="@daily",
    tags=["fetch_twitter"],
) as dag:
    get_twitter_urls = PythonOperator(
        task_id="get_twitter_urls",
        python_callable=FetchTwitter.get_twitter_urls,
        dag=dag,
    )

    fetch_twitter_data = PythonOperator(
        task_id="fetch_twitter_data",
        python_callable=FetchTwitter.run,
        provide_context=True,
        dag=dag,
    )

    get_twitter_urls >> fetch_twitter_data
