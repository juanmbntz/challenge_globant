# Globant Challenge

## Files contained

- backfill.py :
  - This file will take the historic data csv files and run the historical backfill, creating all tables in a bigquery dataset.
  - Note that, in this repository, all csv files are stored inside the "historic_backfill_data" folder, but in the cloud environment, the script is prepared to read those files from a gcs bucket.
  
- api_main.py :
  - Run this script to initialize the Rest API that will process batch inserts in the desired bigquery table.
  - Just for testing purposes, the API is hosted in our cloud shell virtual machine. 
    - To do: Modify the scripts to host the API using a compute engine virtual machine inside our VPC network.

- insert_batch_data.py :
  - Run this file to make POST requests to the API. This job will read files from the "batch_data" folder and insert records in the bigquery tables.
  
- dag_backups.py :
  - This file should be stored inside the cloud composer environment dags folder. The goal of this job is to store daily backups of all tables in AVRO format files that will be kept inside a gcs bucket.
  - In the utils.py module, we have a python function that can be called to restored any bigquery table using the backup file of a specific day.

## Docker
  - Dockerfile : to create a docker image with all required libraries, scripts and files to run our API in a VM or GKE.
  - pus-docker-image.sh : Use this file to push the docker image to google cloud container registry.
  
### Reporting folder:
  - Inside this folder we have 2 SQL scripts to create the tables requested by the stakeholders.
  - There are also 2 visual reports created using GCP Looker Studio. You can request viewer access using the following links:
    - Hirings by quarter: https://datastudio.google.com/reporting/c18d2d2f-2862-4fcd-8f20-2d2541f08d3d
    - Hirings by department: https://datastudio.google.com/reporting/ab37eb82-2dc1-432c-ab34-c450c252836a
