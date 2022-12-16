import requests 

base_url = "http://127.0.0.1:8080/"

response = requests.post(base_url + "post-data-1", {"id": 1,"name": "Juan Manuel"})

print(response.json())