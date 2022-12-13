from google.cloud import bigquery

def csv_to_bq(data_source, table_schema, project_id='fake-project-id', dataset_name='human_resources',  bucket_name='gs://bucket-name'):

    """
    This function takes the GCP project id, bigquery dataset, table name, table schema, source file name and the bucket where 
    the file is located and runs a job to create a bigquery table in the specified dataset with the data contained inside the file

    Assumptions:
        - Files are already located in a GCP bucket.
        - All files are in csv format
    """
    
    client = bigquery.Client()
    table_id = f"{project_id}.{dataset_name}.{data_source}"

    job_config = bigquery.LoadJobConfig(

        schema = table_schema,
        #Assuming the files contain headers
        skip_leading_rows=1,
        #Files format is CSV
        source_format=bigquery.SourceFormat.CSV,
    )

    file_uri = f'/human_resources/{data_source}.csv'
    uri = f"{bucket_name}{file_uri}"

    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )  

    load_job.result()


    