from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator

from utils import backup_table

with DAG(
    "backups",
    description='This dag creates daily backups from bigquery tables',
    schedule_interval="0 0 * * *", 
    start_date=datetime(2022, 12, 16, 0, 0, 0),
    default_args={
        'owner': 'Juan Manuel Benitez',
        'email': 'juanmbntz@gmail.com',
        'retries': 5,
        'depends_on_past': True,
        'max_active_runs': 1
    }
    ) as dag:

    PROJECT = 'project_id'
    DATASET = 'human_resources'
    BUCKET =  'bucket_name' #gs://example-bucket
    BACKUP_DATE = "{{ ds }}"
    employees_table = 'hired_employees'
    departments_table = 'departments'
    jobs_table = 'jobs'


    ini_backups = DummyOperator(
    task_id = 'ini_backups',
    dag=dag,
    wait_for_downstream=True
    )

    backup_employees = PythonOperator(
    task_id='backup_employees',
    dag=dag,
    python_callable=backup_table,
    op_kwargs = {'project': PROJECT, 
                'dataset': DATASET, 
                'table_id': employees_table, 
                'bucket_name': BUCKET, 
                'backup_date': BACKUP_DATE
                }
    )

    backup_departments = PythonOperator(
    task_id='backup_departments',
    dag=dag,
    python_callable=backup_table,
    op_kwargs = {'project': PROJECT, 
                'dataset': DATASET, 
                'table_id': departments_table, 
                'bucket_name': BUCKET, 
                'backup_date': BACKUP_DATE
                }
    )

    backup_jobs = PythonOperator(
    task_id='backup_jobs',
    dag=dag,
    python_callable=backup_table,
    op_kwargs = {'project': PROJECT, 
                'dataset': DATASET, 
                'table_id': jobs_table, 
                'bucket_name': BUCKET, 
                'backup_date': BACKUP_DATE
                }
    ) 

    send_email = EmailOperator(
        task_id="send_email",
        dag=dag,
        to=["juanmbntz@gmail.com"],
        subject="Daily backkups",
        html_content=f" <h3>Backups created succesfully on {{{{ ds }}}}</h3>"
    
    )   
    end_backups = DummyOperator(
    task_id = 'end_backups',
    dag=dag,
    wait_for_downstream=True
    )


ini_backups >> [backup_employees,
                backup_departments,
                backup_jobs] >> send_email >> end_backups