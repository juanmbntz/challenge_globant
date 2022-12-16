#! /bin/bash

#insert employee id: 1, juan manuel benitez, department id: 1 -> data management, job id: 2 -> data engineer

curl -X POST -H "Content-Type: application/json" -d '[{"id":1, "name":"juan manuel benitez","datetime":"2022-12-15T00:00:00Z","department_id":1,"job_id":2}]' http://localhost:8080/post-employee-data

curl -X POST -H "Content-Type: application/json" -d '[{"id":1, "department":"Data Management"}]' http://localhost:8080/post-department-data

curl -X POST -H "Content-Type: application/json" -d '[{"id":2, "job":"Data Engineer"}]' http://localhost:8080/post-job-data