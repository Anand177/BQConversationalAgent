""" Run from Terminal
gcloud auth application-default login           
gcloud auth application-default set-quota-project gcp-project-375309

"""
from google.cloud import bigquery
from pathlib import Path

client = bigquery.Client(project="gcp-project-375309")

header_table_id = "gcp-project-375309.dealer_information.repair_order_header"
labour_table_id = "gcp-project-375309.dealer_information.repair_order_labour"
part_table_id = "gcp-project-375309.dealer_information.repair_order_part"

directory = "../Data/"
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON, autodetect=True,
    write_disposition=bigquery.WriteDisposition.WRITE_APPEND, # Or WRITE_TRUNCATE to overwrite
)

header_json_files = Path(f"{directory}Header/").glob("*.json")
print(Path(f"{directory}Header"))
for file_path in header_json_files:
    print(f"H{file_path}")
    print(f"Reading header File -> {file_path} and loading to {header_table_id}")

    with open(file_path, "rb") as source_file:
        header_load_job = client.load_table_from_file(source_file, header_table_id, 
                                                      job_config=job_config)
    header_load_job.result()  
    print(f"{file_path} successfully loaded to {header_table_id}")
    print(f"Loaded {header_load_job.output_rows} rows into {header_table_id}.")

labour_json_files = Path(f"{directory}Labour").glob("*.json")
for file_path in labour_json_files:
    print(f"Reading labour File -> {file_path} and loading to {labour_table_id}")

    with open(file_path, "rb") as source_file:
        labour_load_job = client.load_table_from_file(source_file, labour_table_id, 
                                                      job_config=job_config)
    labour_load_job.result()  
    print(f"{file_path} successfully loaded to {labour_table_id}")
    print(f"Loaded {labour_load_job.output_rows} rows into {labour_table_id}.")

part_json_files = Path(f"{directory}Part").glob("*.json")
for file_path in part_json_files:
    print(f"Reading part File -> {file_path} and loading to {part_table_id}")

    with open(file_path, "rb") as source_file:
        part_load_job = client.load_table_from_file(source_file, part_table_id, 
                                                      job_config=job_config)
    part_load_job.result()  
    print(f"{file_path} successfully loaded to {part_table_id}")
    print(f"Loaded {part_load_job.output_rows} rows into {part_table_id}.")
