from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.email import send_email
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 0,
}

def send_test_email():
    send_email(
        to=["outlook_CD05F28557E2196B@outlook.com"],
        subject="Airflow SMTP Test Email",
        html_content="""
        <h3>Airflow SMTP is working!</h3>
        <p>This is a test email sent from your Airflow container using Gmail SMTP.</p>
        """
    )
    print("Test email sent")

with DAG(
    dag_id="test_email_smtp_dag",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description="Send a test email to validate SMTP config",
) as dag:

    test_email_task = PythonOperator(
        task_id="send_test_email",
        python_callable=send_test_email
    )
