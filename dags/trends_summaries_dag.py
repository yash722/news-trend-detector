import sys
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Add script path so we can import from scripts/
sys.path.append("/opt/airflow/scripts")

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

def scrape_wrapper():
    from articles_scraper import scrape_articles
    scrape_articles()

# Task 2: Embed & Cluster Articles
def cluster_wrapper():
    from embed_and_cluster_articles import cluster_articles
    cluster_articles()

def summarize_wrapper():
    import pandas as pd
    from summarize_clusters import summarize_clusters

    # Paths inside the container
    input_path = "/opt/airflow/data/clustered/clustered_articles.csv"
    output_path = "/opt/airflow/data/clustered/cluster_summaries.csv"

    summarize_clusters(input_path=input_path, output_path=output_path)

def notif_wrapper():
    from send_notif_whatsapp import send_whatsapp_twilio
    summaries = "/opt/airflow/data/clustered/cluster_summaries.csv"
    send_whatsapp_twilio(summaries)

def notify_streamlit():
    print("Streamlit should now display the latest summaries from cluster_summaries.csv.")

# Define DAG
with DAG(
    "trends_summaries_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    description="Pipeline to scrape, cluster, summarize news, and update dashboard",
) as dag:

    t1 = PythonOperator(task_id="scrape_articles", python_callable=scrape_wrapper)
    t2 = PythonOperator(task_id="cluster_articles", python_callable=cluster_wrapper)
    t3 = PythonOperator(task_id="summarize_clusters", python_callable=summarize_wrapper)
    t4 = PythonOperator(task_id="notify_streamlit", python_callable=notify_streamlit)
    t5 = PythonOperator(task_id="notify_whatsapp", python_callable=notif_wrapper)

    t1 >> t2 >> t3 >> t4 >>t5
