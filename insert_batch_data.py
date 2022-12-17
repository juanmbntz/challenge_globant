import requests
import json
from utils import post_to_api

if __name__ == '__main__':

    #Open json files with the data to be inserted
    employees_file = open('./batch_data/new_employees.json')
    departments_file = open('./batch_data/new_departments.json')
    jobs_file = open('./batch_data/new_jobs.json')

    #POST method requires list of jsons with doulbe quotes
    employees_rows = json.dumps(json.load(employees_file))
    departments_rows = json.dumps(json.load(departments_file))
    jobs_rows = json.dumps(json.load(jobs_file))

    #send POST requests to the API with the desired data
    post_to_api('post-employee-data', employees_rows)
    post_to_api('post-department-data', departments_rows)
    post_to_api('post-job-data', jobs_rows)