from google.cloud import bigquery
import requests
import json


def csv_to_bq(data_source, table_schema, project_id='fake-project-id', dataset_name='human_resources',  bucket_name='gs://bucket-name'):
    """
    This function takes the GCP project id, bigquery dataset, table name, table schema, source file name and the bucket where 
    the file is located and runs a job to create a bigquery table in the specified dataset with the data contained inside the file

    Assumptions:
        - Files are already located in a GCP bucket in the same project:
            - gs://bucket-name/human_resurces/hired_employees.csv
            - gs://bucket-name/human_resurces/departments.csv
            - gs://bucket-name/human_resurces/jobs.csv

        - All files are comma separated
    Args:
        data_source = source of the data (employees, jobs or departments)
        table_schema = schema of the table that we want to create
        project_id = GCP project id
        dataset_name = dataset where the table has to be rewriten
        table_id = table name
        bucket_name = bucket where the historic file is stored
    """
    
    client = bigquery.Client()
    table_id = "{}.{}.{}".format(project_id,dataset_name,data_source)

    job_config = bigquery.LoadJobConfig(
        #schema to be passed when calling the function in the main script
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


def post_to_api(endpoint, data):
    """
    Function to post data in bigquery tables using the Rest API.
    Args:
        endpoint: the endpoint where we are going to post
        data: records that will be inserted in the table
    """

    host_endpoint = 'http://localhost:8080/' + endpoint

    headers = {'Content-Type': 'application/json'}

    #Service is suposed to support only 1000 inserts at once.
    if 1 <= len(data) <= 1000:
        response = requests.post(host_endpoint, headers=headers, data=data)

        print(response.status_code)
    
    else:
        print("You're trying to insert too many records. The limit is set to 1000, please make a smaller request")


from google.cloud import bigquery 

def backup_table(project, dataset, table_id, bucket_name, backup_date):

    """
    Function to backup any bigquery table inside an AVRO file. The file will be stored in a google cloud storage bucket.
    Args:
        project = GCP project id
        dataset = dataset where the table has to be rewriten
        table_id = table name
        bucket_name = bucket where the backup AVRO file is stored
        backup_date = the date of the backup file that we want to use to restore the table
    """
    client = bigquery.Client()

    avro_file = 'gs://{}/backups/backup_{}_{}.avro'.format(bucket_name, table_id, backup_date)

    # dataset and table references
    dataset_ref = client.dataset(dataset, project=project)
    table_ref = dataset_ref.table(table_id)

    # Set the extract job configuration
    job_config = bigquery.job.ExtractJobConfig()
    job_config.destination_format = bigquery.DestinationFormat.AVRO

    extract_job = client.extract_table(
            table_ref,
            avro_file,
            job_config=job_config,
            )  

    #execute request
    extract_job.result() 


def restore_from_backup(project, dataset, table_id, bucket_name, backup_date):
    
    """
    Function to restore any bigquery table using a specific AVRO file containing a backup.
    Args:
        project = GCP project id
        dataset = dataset where the table has to be rewriten
        table_id = table name
        bucket_name = bucket where the backup AVRO file is stored
        backup_date = the date of the backup file that we want to use to restore the table
    """
    client = bigquery.Client()

    # Set our load job configuration
    job_config = bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.AVRO)
    #Set write mode to truncate + write so we first empty the table in order to rewrite it with our backup
    job_config.write_disposition = 'WRITE_TRUNCATE'

    avro_file = 'gs://{}/backups/backup_{}_{}.avro'.format(bucket_name, table_id, backup_date)

    # table to be restored
    destination_table = '{}.{}.{}'.format(project, dataset, table_id)

    load_job = client.load_table_from_uri(
        avro_file, destination_table, job_config=job_config
    ) 

    #execute request
    load_job.result()
