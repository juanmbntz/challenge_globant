from flask import Flask, request
from google.cloud import bigquery

# Create Flask object
app = Flask(__name__)

# Set bigquery client
client = bigquery.Client()

# table names:
table_1_name = "proyect-id.dataset.table-1-name"
table_2_name = "proyect-id.dataset.table-2-name"

# Create a table reference.
table_ref_1 = client.dataset('dataset').table('table-1-name')
table_ref_2 = client.dataset('dataset').table('table-2-name')

table_1 = bigquery.Table(table_ref_1)
table_2 = bigquery.Table(table_ref_2)


table_1.schema = [
    bigquery.SchemaField("id", "INTEGER"),
    bigquery.SchemaField("name", "STRING"),
]

table_2.schema = [
    bigquery.SchemaField("id", "INTEGER"),
    bigquery.SchemaField("first_name", "STRING"),
    bigquery.SchemaField("last_name", "STRING"),


]

# Define the endpoint for posting data to the table.
@app.route("/post-data-1", methods=["POST"])
def post_data_1():
   
    data = request.get_json()

    
    errors = client.insert_rows(table_1, data)

    
    if errors == []:
        return "Data was posted successfully to the table 1.", 200
    else:
        return "Errors occurred while posting data to the table 1: " + str(errors), 400

@app.route("/post-data-2", methods=["POST"])
def post_data_2():
    
    data = request.get_json()

    errors = client.insert_rows(table_2, data)

    if errors == []:
        return "Data was posted successfully to the table 2.", 200
    else:
        return "Errors occurred while posting data to the table 2: " + str(errors), 400

# Run 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

