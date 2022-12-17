# Globant Challenge

## Files contained

- backfill.py :
  - This file will take the historic data csv files and run the historical backfill, creating all tables in a bigquery dataset.
  - Note that, in this repository, all csv files are stored inside the "historic_backfill_data" folder, but in the cloud environment, the script is prepared to read those files from a gcs bucket.
  
- api_main.py :
  - Run this script to initialize the Rest API that will process batch inserts in the desired bigquery table.
  - To do: Modify the scripts to host the API using a compute engine virtual machine inside our VPC network.

- insert_batch_data.py :
  - Run this file to make POST requests to the API. This job will read files from the "batch_data" folder and insert records in the bigquery tables.
  
- dag_backups.py :
  - This file should be stored inside the cloud composer environment dags folder. The goal of this job is to store daily backups of all tables in AVRO format files that will be kept inside a gcs bucket.
  - In the utils.py module, we have a python function that can be called to restored any bigquery table using the backup file of a specific day.

  
 
