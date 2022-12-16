from flask import Flask, request
from google.cloud import bigquery

# Create Flask object
app = Flask(__name__)

# Set bigquery client
client = bigquery.Client()

"""
Assumptions:
    - proyect is set to default
    - dataset name: human_resources
    - tables names:
        - employees table name: hired_employees
        - departments table name: departments
        - jobs table name: jobs
"""
# Set table references

# hired employees
hired_employees_table_ref = client.dataset('human_resources').table('hired_employees')
# departments
departments_table_ref = client.dataset('human_resources').table('departments')
# jobs
jobs_table_ref = client.dataset('human_resources').table('jobs')

hired_employees_table = bigquery.Table(hired_employees_table_ref)
departments_table = bigquery.Table(departments_table_ref)
jobs_table = bigquery.Table(jobs_table_ref)

# Tables schemas 
hired_employees_table.schema = [
    bigquery.SchemaField("id", "INTEGER", mode = "REQUIRED"),
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("datetime", "STRING"),
    bigquery.SchemaField("department_id", "INTEGER"),
    bigquery.SchemaField("job_id", "INTEGER"),
]

departments_table.schema = [
    bigquery.SchemaField("id", "INTEGER", mode = "REQUIRED"),
    bigquery.SchemaField("department", "STRING"),
]

jobs_table.schema = [
    bigquery.SchemaField("id", "INTEGER", mode = "REQUIRED"),
    bigquery.SchemaField("job", "STRING"),
]

# Define the endpoint for posting employees data
@app.route("/post-employee-data", methods=["POST"])
def post_data_1():
   
    # Get the date on the request
    data = request.get_json()

    # Store errors if ocurred
    errors = client.insert_rows(hired_employees_table, data)

    
    if errors == []:
        return "Data was posted successfully to the hired employees table.", 200
    else:
        return "Errors occurred while posting data to the hired employees table: " + str(errors), 400

# Endpoint for departments posting
@app.route("/post-department-data", methods=["POST"])
def post_data_2():
    
    # Get the date on the request
    data = request.get_json()

    # Store errors if ocurred
    errors = client.insert_rows(departments_table, data)

    if errors == []:
        return "Data was posted successfully to the departments table.", 200
    else:
        return "Errors occurred while posting data to the departments table: " + str(errors), 400

# Endpoint for jobs posting
@app.route("/post-job-data", methods=["POST"])
def post_data_2():
    
    # Get the date on the request
    data = request.get_json()

    # Store errors if ocurred
    errors = client.insert_rows(jobs_table, data)

    if errors == []:
        return "Data was posted successfully to the jobs table.", 200
    else:
        return "Errors occurred while posting data to the jobs table: " + str(errors), 400


# Run on port 8080 (flask default)
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)

