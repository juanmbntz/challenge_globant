from utils import csv_to_bq
from google.cloud import bigquery


if __name__=='__main__':
    
    hired_employees_schema = [
            bigquery.SchemaField("id", "INTEGER", mode = "REQUIRED"),
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("datetime", "STRING"),
            bigquery.SchemaField("department_id", "INTEGER"),
            bigquery.SchemaField("job_id", "INTEGER"),
            ]

    departments_schema =  [
            bigquery.SchemaField("id", "INTEGER", mode = "REQUIRED"),
            bigquery.SchemaField("department", "STRING"),
            ]

    jobs_schema = [
            bigquery.SchemaField("id", "INTEGER", mode = "REQUIRED"),
            bigquery.SchemaField("job", "STRING"),
            ]

    #hired employees
    csv_to_bq(data_source='hired_employees', table_schema=hired_employees_schema)

    #departments
    csv_to_bq(data_source='departments', table_schema=departments_schema)

    #jobs
    csv_to_bq(data_source='jobs', table_schema=jobs_schema)