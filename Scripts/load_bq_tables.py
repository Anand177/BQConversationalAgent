""" Run from Terminal
gcloud auth application-default login           
gcloud auth application-default set-quota-project gcp-project-375309

"""
from google.cloud import bigquery
from pathlib import Path

client = bigquery.Client(project="gcp-project-375309")
directory = "BQConversationalAgent/Data/"

header_table_id = "gcp-project-375309.dealer_information.repair_order_header"
labour_table_id = "gcp-project-375309.dealer_information.repair_order_labour"
part_table_id = "gcp-project-375309.dealer_information.repair_order_part"

header_schema = [
    bigquery.SchemaField("country_code", "STRING", "REQUIRED"),
    bigquery.SchemaField("dealer_code", "STRING", "REQUIRED"),
    bigquery.SchemaField("dealer_sub_code", "STRING"),
    bigquery.SchemaField("ro_number", "STRING", "REQUIRED"),  
    bigquery.SchemaField("ro_open_date", "DATE", "REQUIRED"),
    bigquery.SchemaField("ro_close_date", "DATE", "REQUIRED"),
    bigquery.SchemaField("ro_process_date", "DATE", "REQUIRED"),
    bigquery.SchemaField("skip_flag", "STRING"),
    bigquery.SchemaField("vin", "STRING", "REQUIRED"),
    bigquery.SchemaField("customer_flag", "STRING", "REQUIRED"),
    bigquery.SchemaField("customer_first_name", "STRING"),
    bigquery.SchemaField("customer_last_name", "STRING", "REQUIRED"),
    bigquery.SchemaField("customer_address_1", "STRING"),
    bigquery.SchemaField("customer_address_2", "STRING"),
    bigquery.SchemaField("customer_city", "STRING"),
    bigquery.SchemaField("customer_state", "STRING"),
    bigquery.SchemaField("customer_zip", "STRING"),
    bigquery.SchemaField("customer_country", "STRING"),
    bigquery.SchemaField("customer_home_phone", "STRING"),
    bigquery.SchemaField("customer_work_phone", "STRING"),
    bigquery.SchemaField("customer_cell_phone", "STRING"),
    bigquery.SchemaField("customer_sms_phone", "STRING"),
    bigquery.SchemaField("customer_mms_phone", "STRING"),
    bigquery.SchemaField("customer_email", "STRING"),
    bigquery.SchemaField("service_advisor_code", "STRING", "REQUIRED"),
    bigquery.SchemaField("customer_type", "STRING"),
    bigquery.SchemaField("derived_customer_type", "STRING"),
    bigquery.SchemaField("odometer_reading", "INTEGER", "REQUIRED"),
    bigquery.SchemaField("odometer_code", "STRING"),
    bigquery.SchemaField("customer_paid_part_amount", "NUMERIC"),
    bigquery.SchemaField("customer_paid_labour_amount", "NUMERIC"),
    bigquery.SchemaField("customer_paid_misc_amount", "NUMERIC"),
    bigquery.SchemaField("customer_paid_tax_amount", "NUMERIC"),
    bigquery.SchemaField("customer_paid_net_amount", "NUMERIC"),
    bigquery.SchemaField("total_part_amount", "NUMERIC"),
    bigquery.SchemaField("total_labour_amount", "NUMERIC"),
    bigquery.SchemaField("total_misc_amount", "NUMERIC"),
    bigquery.SchemaField("total_tax_amount", "NUMERIC"),
    bigquery.SchemaField("total_net_amount", "NUMERIC"),
]

labour_schema = [
    bigquery.SchemaField("country_code", "STRING", "REQUIRED"),
    bigquery.SchemaField("dealer_code", "STRING", "REQUIRED"),
    bigquery.SchemaField("dealer_sub_code", "STRING"),
    bigquery.SchemaField("ro_number", "STRING", "REQUIRED"),  
    bigquery.SchemaField("ro_open_date", "DATE", "REQUIRED"),
    bigquery.SchemaField("ro_close_date", "DATE", "REQUIRED"),
    bigquery.SchemaField("ro_process_date", "DATE", "REQUIRED"),
    bigquery.SchemaField("skip_flag", "STRING"),
	bigquery.SchemaField("service_job_number", "INTEGER", "REQUIRED"),
    bigquery.SchemaField("service_sequence_number", "INTEGER", "REQUIRED"),
    bigquery.SchemaField("original_repair_type_code", "STRING", "REQUIRED"),
    bigquery.SchemaField("derived_repair_type_code", "STRING"),
    bigquery.SchemaField("react_category_code", "STRING"),
    bigquery.SchemaField("original_labour_op_code", "STRING"),
    bigquery.SchemaField("standard_labour_op_code", "STRING"),
    bigquery.SchemaField("service_hours", "NUMERIC"),
    bigquery.SchemaField("customer_paid_labour_amount", "NUMERIC")
]
part_schema = [
    bigquery.SchemaField("country_code", "STRING", "REQUIRED"),
    bigquery.SchemaField("dealer_code", "STRING", "REQUIRED"),
    bigquery.SchemaField("dealer_sub_code", "STRING"),
    bigquery.SchemaField("ro_number", "STRING", "REQUIRED"),  
    bigquery.SchemaField("ro_open_date", "DATE", "REQUIRED"),
    bigquery.SchemaField("ro_close_date", "DATE", "REQUIRED"),
    bigquery.SchemaField("ro_process_date", "DATE", "REQUIRED"),
    bigquery.SchemaField("skip_flag", "STRING"),
	bigquery.SchemaField("service_job_number", "INTEGER", "REQUIRED"),
    bigquery.SchemaField("service_sequence_number", "INTEGER", "REQUIRED"),
    bigquery.SchemaField("part_sequence_number", "INTEGER", "REQUIRED"),
    bigquery.SchemaField("packed_part_code", "STRING"),
    bigquery.SchemaField("customer_paid_part_amount", "NUMERIC")]

header_job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON, schema = header_schema,
    autodetect=False, write_disposition=bigquery.WriteDisposition.WRITE_APPEND, 
)
labour_job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON, schema = labour_schema,
    autodetect=False, write_disposition=bigquery.WriteDisposition.WRITE_APPEND, 
)
part_job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON, schema = part_schema,
    autodetect=False, write_disposition=bigquery.WriteDisposition.WRITE_APPEND, 
)

header_json_files = Path(f"{directory}Header/").glob("*.json")
print(Path(f"{directory}Header"))
for file_path in header_json_files:
    print(f"H{file_path}")
    print(f"Reading header File -> {file_path} and loading to {header_table_id}")

    with open(file_path, "rb") as source_file:
        header_load_job = client.load_table_from_file(source_file, header_table_id, 
                    job_config=header_job_config)
    header_load_job.result()  
    print(f"{file_path} successfully loaded to {header_table_id}")
    print(f"Loaded {header_load_job.output_rows} rows into {header_table_id}.")

labour_json_files = Path(f"{directory}Labour").glob("*.json")
for file_path in labour_json_files:
    print(f"Reading labour File -> {file_path} and loading to {labour_table_id}")

    with open(file_path, "rb") as source_file:
        labour_load_job = client.load_table_from_file(source_file, labour_table_id, 
                    job_config=labour_job_config)
    labour_load_job.result()  
    print(f"{file_path} successfully loaded to {labour_table_id}")
    print(f"Loaded {labour_load_job.output_rows} rows into {labour_table_id}.")

part_json_files = Path(f"{directory}Part").glob("*.json")
for file_path in part_json_files:
    print(f"Reading part File -> {file_path} and loading to {part_table_id}")

    with open(file_path, "rb") as source_file:
        part_load_job = client.load_table_from_file(source_file, part_table_id, 
                    job_config=part_job_config)
    part_load_job.result()  
    print(f"{file_path} successfully loaded to {part_table_id}")
    print(f"Loaded {part_load_job.output_rows} rows into {part_table_id}.")
