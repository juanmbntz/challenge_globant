#! /bin/bash

curl -X POST -H "Content-Type: application/json" -d '[{"id":3, "name":"juan"},{"id":4, "name":"manuel"}]' http://localhost:8080/post-data-1

curl -X POST -H "Content-Type: application/json" -d '[{"id":1, "first_name":"juan manuel","last_name":"benitez" },{"id":2, "first_name":"juan manuel","last_name":"benitez" }]' http://localhost:8080/post-data-2

