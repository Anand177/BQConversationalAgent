-- =============================================================================
-- Automobile Repair Order (RO) data model - BigQuery DDL
-- Replace `gcp-project-375309.dealer_information` with your project and dataset.
--
-- Relationships (all joins are on the full composite key):
--   repair_order_header  1 --- N  repair_order_labour  1 --- 0..N  repair_order_part
--
--   header -> labour : country_code, dealer_code, ro_number, ro_open_date
--   labour -> part   : country_code, dealer_code, ro_number, ro_open_date,
--                      service_job_number, service_sequence_number
--
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. HEADER: one row per repair order (RO). Overall RO, vehicle, customer, totals.
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE `gcp-project-375309.dealer_information.repair_order_header` (
  -- Keys
  country_code STRING(3) NOT NULL OPTIONS(description="Country code of the dealer that opened the repair order. Part of the composite key shared by header, labour and part tables. Source: country"),
  dealer_code STRING(5) NOT NULL OPTIONS(description="Dealer identifier that owns the repair order. Part of the composite key shared by all repair order tables. Source: dealer"),
  dealer_sub_code STRING(3) OPTIONS(description="Dealer sub-code identifying the dealer location or department. Part of the composite key shared by all repair order tables. Source: dealer_sub_code"),
  ro_number STRING(16) NOT NULL OPTIONS(description="Repair order number, unique within a country, dealer and dealer sub-code. Identifies one service visit. Source: ro"),

  -- Dates
  ro_open_date DATE OPTIONS(description="Date the repair order was opened, i.e. when the vehicle was checked in for service. Source: open_date"),
  ro_close_date DATE OPTIONS(description="Date the repair order was closed, i.e. when service was completed and invoiced. Source: close_date"),
  ro_process_date DATE OPTIONS(description="Date the repair order record was processed or loaded into the data platform. Preferred column for service-date. Source: process_date"),

  -- Record flags and vehicle
  skip_flag STRING(1) OPTIONS(description="Flag indicating whether the record is marked to be skipped or excluded from downstream processing. Only consider records where this column is empty or 'N'. Skip all records with this column 'Y'. Same meaning in the labour and part tables. Source: skip_flag"),
  vin STRING(17) OPTIONS(description="Vehicle Identification Number (VIN) of the serviced vehicle. Use to find all repair orders for one vehicle. Source: vin"),

  -- Customer (contains PII)
  customer_flag STRING(1) OPTIONS(description="Flag indicating the customer type. I -> Individual, O -> Company/ organization Source: customer_flag"),
  customer_first_name STRING(50) OPTIONS(description="PII. Customer first name. Source: customer_first_name"),
  customer_last_name STRING(50) OPTIONS(description="PII. Customer last name if the customer_flag is 'I'. Company name if customer_flag is 'O'.  Source: customer_last_name"),
  customer_address_1 STRING(100) OPTIONS(description="PII. Customer street address, line 1. Source: customer_address_1"),
  customer_address_2 STRING(100) OPTIONS(description="PII. Customer street address, line 2 (apartment, suite, etc.). Source: customer_address_2"),
  customer_city STRING(50) OPTIONS(description="Customer city. Source: customer_city"),
  customer_state STRING(50) OPTIONS(description="Customer state or province. Source: customer_state"),
  customer_zip STRING(20) OPTIONS(description="Customer postal or ZIP code. Stored as STRING to preserve leading zeros. Source: customer_zip"),
  customer_country STRING(3) OPTIONS(description="Country of the customer address. May differ from country_code, which is the dealer's country. Source: customer_country"),
  customer_home_phone STRING(25) OPTIONS(description="PII. Customer home phone number. Source: customer_home_phone"),
  customer_work_phone STRING(25) OPTIONS(description="PII. Customer work phone number. Source: customer_work_phone"),
  customer_cell_phone STRING(25) OPTIONS(description="PII. Customer mobile phone number. Source: customer_cell_phone"),
  customer_sms_phone STRING(25) OPTIONS(description="PII. Customer phone number used for SMS text messages. Source: customer_sms_phone"),
  customer_mms_phone STRING(25) OPTIONS(description="PII. Customer phone number used for MMS multimedia messages. Source: customer_mms_phone"),
  customer_email STRING(80) OPTIONS(description="PII. Customer email address. Source: customer_email"),
  service_advisor_code STRING(20) OPTIONS(description="Code of the service advisor who handled the repair order. Source: service_advisor_code"),
  customer_type STRING(2) OPTIONS(description="Customer type code as recorded in the source dealer system, e.g. retail or fleet. Source: customer_type"),
  derived_customer_type STRING(2) OPTIONS(description="Customer type derived or standardized by the data platform. Prefer this over customer_type for consistent segmentation across dealers. Source: derived_customer_type"),

  -- Odometer
  odometer_reading INT64 OPTIONS(description="Vehicle odometer reading at check-in. Interpret the unit using odometer_code. Source: odometer_reading"),
  odometer_code STRING(1) OPTIONS(description="Code for the unit of odometer_reading, e.g. miles or kilometers. Source: odometer_code"),

  -- Amounts paid by the customer
  customer_paid_part_amount NUMERIC OPTIONS(description="Parts amount paid by the customer on this repair order. Excludes amounts paid by other parties such as warranty. Source: customer_paid_part_amount"),
  customer_paid_labour_amount NUMERIC OPTIONS(description="Labour amount paid by the customer on this repair order. Equals the sum of labour-level customer_paid_labour_amount. Source: customer_paid_labour_amount"),
  customer_paid_misc_amount NUMERIC OPTIONS(description="Miscellaneous charges (shop supplies, fees, etc.) paid by the customer on this repair order. Source: customer_paid_misc_amount"),
  customer_paid_tax_amount NUMERIC OPTIONS(description="Tax paid by the customer on this repair order. Source: customer_paid_tax_amount"),
  customer_paid_net_amount NUMERIC OPTIONS(description="Net total paid by the customer on this repair order, i.e. parts, labour, misc and tax combined. Source: customer_paid_net_amount"),

  -- Total repair order amounts (all payers)
  total_part_amount NUMERIC OPTIONS(description="Total parts amount on the repair order across all payers (customer, warranty, internal). Source: total_part_amount"),
  total_labour_amount NUMERIC OPTIONS(description="Total labour amount on the repair order across all payers (customer, warranty, internal). Source: total_labour_amount"),
  total_misc_amount NUMERIC OPTIONS(description="Total miscellaneous charges on the repair order across all payers. Source: total_misc_amount"),
  total_tax_amount NUMERIC OPTIONS(description="Total tax on the repair order across all payers. Source: total_tax_amount"),
  total_net_amount NUMERIC OPTIONS(description="Net total value of the repair order across all payers, i.e. parts, labour, misc and tax combined. Use for overall repair order revenue. Source: total_net_amount"),

  PRIMARY KEY (country_code, dealer_code, ro_number, ro_open_date) NOT ENFORCED
)
PARTITION BY ro_open_date
CLUSTER BY country_code, dealer_code, ro_number
OPTIONS(
  description="Repair order header. One row per automobile service repair order (one service visit of a vehicle at a dealer). Holds overall repair order information: dealer, open/close/process dates, vehicle VIN, odometer, customer contact details (PII), service advisor, and the customer-paid and total amounts for parts, labour, misc, tax and net. Start here for questions about visits, customers, vehicles and revenue per repair order. Parent of repair_order_labour (one header row to one or many labour rows). Join on country_code, dealer_code, ro_number.",
  labels=[("domain", "automotive_service"), ("entity", "repair_order"), ("grain", "one_row_per_ro")]
);


-- -----------------------------------------------------------------------------
-- 2. LABOUR: one row per service line (job/sequence) performed on a repair order.
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE `gcp-project-375309.dealer_information.repair_order_labour` (
  -- Keys (link to repair_order_header)
  country_code STRING(3) NOT NULL OPTIONS(description="Country code of the dealer. Foreign key to repair_order_header.country_code. Source: country"),
  dealer_code STRING(5) NOT NULL OPTIONS(description="Dealer identifier. Foreign key to repair_order_header.dealer_code. Source: dealer"),
  dealer_sub_code STRING(3) OPTIONS(description="Dealer sub-code. Foreign key to repair_order_header.dealer_sub_code. Source: dealer_sub_code"),
  ro_number STRING(16) NOT NULL OPTIONS(description="Repair order number. Foreign key to repair_order_header.ro_number. Source: ro"),
  service_job_number INT64 NOT NULL OPTIONS(description="Job number of the service line within the repair order. Together with service_sequence_number it uniquely identifies a labour line, and it links to repair_order_part. Source: service_job_number"),
  service_sequence_number INT64 NOT NULL OPTIONS(description="Sequence number of the labour line within the service job. Together with service_job_number it uniquely identifies a labour line, and it links to repair_order_part. Source: service_sequence_number"),

  -- Dates (copied from the header)
  ro_open_date DATE OPTIONS(description="Date the parent repair order was opened. Same value as repair_order_header.ro_open_date. Source: open_date"),
  ro_close_date DATE OPTIONS(description="Date the parent repair order was closed. Same value as repair_order_header.ro_close_date. Source: close_date"),
  ro_process_date DATE OPTIONS(description="Date the record was processed or loaded into the data platform. Preferred column for service-date. Source: process_date"),
  skip_flag STRING(1) OPTIONS(description="Flag indicating whether the record is marked to be skipped or excluded from downstream processing. Only consider records where this column is empty or 'N'. Skip all records with this column 'Y'. Source: skip_flag"),

  -- Service classification
  original_repair_type_code STRING(1) OPTIONS(description="Repair type code exactly as entered in the dealer system, e.g. customer pay, warranty or internal. Source: original_repair_type_code"),
  derived_repair_type_code STRING(1) OPTIONS(description="Repair type code standardized by the data platform. Prefer this over original_repair_type_code for consistent cross-dealer analysis. Source: derived_repair_type_code"),
  react_category_code STRING(20) OPTIONS(description="REACT category code that classifies the type of service or repair performed on this labour line. Source: react_category_code"),
  original_labour_op_code STRING(120) OPTIONS(description="Labour operation code exactly as entered in the dealer system. Identifies the service operation performed. Source: original_labour_op_code"),
  standard_labour_op_code STRING(80) OPTIONS(description="Labour operation code standardized by the data platform. Prefer this over original_labour_op_code to compare the same operation across dealers. Source: standard_labor_op_code"),

  -- Measures
  service_hours NUMERIC OPTIONS(description="Labour hours charged or recorded for this service line. Source: service_hours"),
  customer_paid_labour_amount NUMERIC OPTIONS(description="Labour amount paid by the customer for this service line. Sum by repair order to reconcile with repair_order_header.customer_paid_labour_amount. Source: customer_paid_labour_amount"),

  PRIMARY KEY (country_code, dealer_code, ro_number, ro_open_date, service_job_number, service_sequence_number) NOT ENFORCED,
  FOREIGN KEY (country_code, dealer_code, ro_number, ro_open_date)
    REFERENCES `gcp-project-375309.dealer_information.repair_order_header` (country_code, dealer_code, ro_number, ro_open_date) NOT ENFORCED
)
PARTITION BY ro_open_date
CLUSTER BY country_code, dealer_code, ro_number
OPTIONS(
  description="Repair order labour lines. One row per service line (job and sequence) performed on a vehicle as part of a repair order, with repair type, labour operation code, service hours and customer-paid labour amount. Child of repair_order_header: one header row maps to one or many labour rows (join on country_code, dealer_code, ro_number). Parent of repair_order_part: one labour row maps to zero or many part rows (also join on service_job_number and service_sequence_number). Use for questions on what services were done, labour hours and operation mix.",
  labels=[("domain", "automotive_service"), ("entity", "repair_order_labour"), ("grain", "one_row_per_labour_line")]
);


-- -----------------------------------------------------------------------------
-- 3. PART: one row per part used on a labour line.
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE `gcp-project-375309.dealer_information.repair_order_part` (
  -- Keys (link to repair_order_labour and repair_order_header)
  country_code STRING(3) NOT NULL OPTIONS(description="Country code of the dealer. Foreign key to repair_order_labour.country_code. Source: country"),
  dealer_code STRING(5) NOT NULL OPTIONS(description="Dealer identifier. Foreign key to repair_order_labour.dealer_code. Source: dealer"),
  dealer_sub_code STRING(3) OPTIONS(description="Dealer sub-code. Foreign key to repair_order_labour.dealer_sub_code. Source: dealer_sub_code"),
  ro_number STRING(16) NOT NULL OPTIONS(description="Repair order number. Foreign key to repair_order_labour.ro_number and repair_order_header.ro_number. Source: ro"),
  service_job_number INT64 NOT NULL OPTIONS(description="Job number of the labour line this part was used on. Foreign key to repair_order_labour.service_job_number. Source: service_job_number"),
  service_sequence_number INT64 NOT NULL OPTIONS(description="Sequence number of the labour line this part was used on. Foreign key to repair_order_labour.service_sequence_number. Source: service_sequence_number"),
  part_sequence_number INT64 NOT NULL OPTIONS(description="Sequence number of the part was used on the labour line. Source: part_sequence_number"),

  -- Dates (copied from the header)
  ro_open_date DATE OPTIONS(description="Date the parent repair order was opened. Same value as repair_order_header.ro_open_date. Source: open_date"),
  ro_close_date DATE OPTIONS(description="Date the parent repair order was closed. Same value as repair_order_header.ro_close_date. Source: close_date"),
  ro_process_date DATE OPTIONS(description="Date the record was processed or loaded into the data platform. Preferred column for service-date. Source: process_date"),
  skip_flag STRING(1) OPTIONS(description="Flag indicating whether the record is marked to be skipped or excluded from downstream processing. Only consider records where this column is empty or 'N'. Skip all records with this column 'Y'. Source: skip_flag"),

  -- Part details
  packed_part_code STRING(23) OPTIONS(description="Packed (condensed) code identifying the part used on the service line. Use it to group parts and analyze part usage. Not a row identifier: the same code can appear many times. Source: packed_part_code"),
  customer_paid_part_amount NUMERIC OPTIONS(description="Parts amount paid by the customer for this part line. Sum by repair order to reconcile with repair_order_header.customer_paid_part_amount. Source: customer_paid_part_amount"),

 PRIMARY KEY (country_code, dealer_code, ro_number, ro_open_date, service_job_number, service_sequence_number) NOT ENFORCED,
 FOREIGN KEY (country_code, dealer_code, ro_number, ro_open_date)
   REFERENCES `gcp-project-375309.dealer_information.repair_order_header` (country_code, dealer_code, ro_number, ro_open_date) NOT ENFORCED

)
PARTITION BY ro_open_date
CLUSTER BY country_code, dealer_code, ro_number
OPTIONS(
  description="Repair order parts. One row per part used on a labour line of a repair order, with packed part code and customer-paid part amount. Child of repair_order_labour: one labour row maps to zero or many part rows (join on country_code, dealer_code, ro_number, service_job_number, service_sequence_number). Use for questions on which parts were used, part cost to the customer and part usage per service operation. Join through repair_order_labour to reach repair_order_header details.",
  labels=[("domain", "automotive_service"), ("entity", "repair_order_part"), ("grain", "one_row_per_part_line")]
);