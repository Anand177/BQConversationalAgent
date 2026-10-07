import pandas as pd
import random
from datetime import date, datetime, timedelta
from faker import Faker

fake = Faker()
num_rows = 1000
start_date = datetime(2025,1,1)
end_date = date.today()

country_list = ['USA', 'CAN']
cust_type_dict = {
    "A":"B",    "B":"B",    "C":"C",    "E":"C",    "D":"D",    "H":"D",    "F":"F",    "L":"F",
    "G":"G",    "M":"G",    "I":"I",    "O":"I",    "J":"J",    "Q":"J",    "K":"K",    "R":"K",
    "N":"N",    "S":"N",    "P":"P",    "T":"P",    "W":"W",    "U":"W",
}

repair_type_dict = {
    'C': 'C',   'I': 'I',   'W': 'W',   'E': 'C',   'W': 'F',   'W': 'C',   'U': 'U',   'C': 'F',
    'I': 'C',   'I': 'F',   'C': 'W',   'A': 'A',   'I': 'W',   'N': 'C',   'E': 'W'
}

labour_op_code_dict = {
    '13529989' : 'GREEN BATTERY GBATT',
    '99P' : '3PERFORM MULTI-POINT INSPECTION',
    'GTIRE' : 'GREEN TIRE',
    'GBRAKE' : 'GREEN BRAKE',
    '9601A' : 'REPLACE AIR FILTER',
    'STATE INSP' : 'STATE INSPECTION',
    'MAINTENANCE' : 'BASIC MAINTENANCE SERVICE - K',
    '1007D3T' : 'TIRE ROTATION',
    'ACCESSORIES' : 'ACCESSORIES',
    '17528A' : 'REPLACE WIPER BLADES',
    'BODY SHOP' : 'BODY REPAIR',
    'ENGINE LGHT' : 'CHECK ENGINE LIGHT',
    'AL4W' : '4 WHEEL ALIGNMENT',
    '6731A' : 'ENGINE OIL AND OIL FILTER - REPLACE',
    '10654B' : 'REPLACE BATTERY',
    '12650D' : 'EEC SYSTEM DIAGNOSIS',
    'PREDLVINSP' : 'PRE-DELIVERY INSPECTION',
    '12651D45' : 'BODY/CHASSIS/ELECTRICAL - DIAGNOSTIC PIN POINT TEST',
    '10654C' : 'BATTERY - TEST, CHARGE, AND RE-TEST',
    'WASH' : 'WASH VEHICLE'
}

packed_part_code_list : list[str] = ['L9YCV37TKL22C1', '7N23GWBRU03J', 'J3CIBE78N', 
    'EN6OKWFVK9G90A', 'JW3FN4ZKC5R78', '5TTUM6XVHN', '3ZPAVHYTTNCB', 'E1YD665KTKEE', 
    '4KJO5OHPIQR8ICC7W', 'VP2IRLXCW4D', '7VHDHGULQ6', 'LWIF3FLJWOWM', 'XRD8ULL7B7X', 
    'NGD3PP268CN02', 'GFXV4X5H7', 'KEDK0TSIQBQ7EH1YTG', '6241P0063', 'KJXDCXFALG', '51KSLDG1TFY', 
    '2O1COYCFU9', 'WAS4F7OI7ZXHBO', 'D7AD4TL8BUQRU8M', 'T64EG1MOD9KYP0N', 'XVT668CZSIUI7ED', 
    'RUZ51MX0A', '0R3VBCFIZY2YD0L', 'WHY5B7PHC', '47P3I4NMOYYOX6AQOF', '6H3YIGKMVSPUE70', 
    'L1KM3EFE3X7', 'BQGPDKXQ6CS', 'SF63IG2P9', 'FGMZ8HP96C9U', 'VB1TJEYPAYPQ8U3',
    '173BV8KE7ZUPY4ABL', '6VCFFWHJX8QY7', 'PALJRRZQZPPNAQ4', 'VJERO23TX', 'Z71YTUH2DCPBR5L04', 
    'WPZTO4OHERERL', '1UCQWCL5R0', 'S2CN4PVMSUMD', '5YDUN93SRVIVUL5', 'ECNUZ32FHC0MRH', 
    '7W34N2Z49LD', 'R10FM8CMJD1', 'VTTJ2SX2C', '4O748DDG52', 'F0K293W6GZ', 'W7T6RAHUD4YOMIY', 
    '0CQOZ0GN1HNSRVKG', 'MI592AI2P8Q', 'X7SUX10WDI1STI1', '8KBWLP8DK07', '2YUV019OGCSPU9', 
    'DVLCTUKSZC5ES', 'GGTRNTMLN', '16LFWYML8B', 'BFCFPLVW6KMRTBD2VN', 'LUSPYI97I', 
    '94707F7595TDDQLLWD', 'PIKEHO3G2LWF8N7LD9', 'OWXRLQ8HUGSLR', 'WKV6XWI0VNA15B', '68L02PSRFSU1', 
    'GTKNIDFGN', 'UUX5RBFPASWT8X', 'OHM85ELYG3O936XVJ3', '9KO6LM1E5NURDA5X99', 'ZZX27JP48N',
    'OULXJK67AQTAU', '7BY5KW4UFLQ', 'NFVCKZ9H22VC8ETE3H', 'D5R38ASIE', 'HTMK7EJM30Q', 'U3SY4YKEP5Y',
    'SGSBEI0N2O', '6S5QOTWX4UNFUFXO', 'NTFJJ9JPD0', 'RF47B5K7X6WODE7DD', '4IPN07RZ3X737FEV', 
    'HPK09QQSLJT8', 'JC96M044W3KBF91D', 'SYJWH7YOJE', 'CF1JB9HN5U74333', '24OLUJ8ER1WKX', 
    'WTHHQSEOL2X2CH3K', '9C81IGSYROX7W', 'E5I9H7F3HF', 'YOUAA2R2F03M88OWP', 'R2S52V7KDGCC', 
    'EIN9GIU2V', '4UB843XD5KLD7R', '0X51NYVNF1PX4SXP', 'VPS2SOZPKG', 'W96FFJYTK95PTB', '6TEEP0836', 
    'NPDPX9307Z', 'Z1T2J78GVXFT4P0ED', 'M51H1W4RATQV']

def generate_number(numbers : list[int], weights : list[int], k : int) -> int:
    return random.choices(numbers, weights=weights, k=k)[0]

def generate_labor_number() -> int:
    numbers = [0, 1, 2, 3, 4, 5, 6]
    weights = [0, 5, 50, 30, 10, 3, 2]
    return generate_number(numbers, weights=weights, k=1)

def generate_labor_service_number() -> int:
    numbers = [0, 1, 2, 3]
    weights = [0, 60, 25, 15]
    return generate_number(numbers, weights=weights, k=1)

def generate_part_number() -> int:
    numbers = [0, 1, 2, 3]
    weights = [0, 60, 25, 15]
    return generate_number(numbers, weights=weights, k=1)

ro_header_country_list: list[str] = []
ro_header_dealer_list: list[str] = []
ro_header_dealer_sub_code_list: list[str] = []
ro_header_ro_list : list[str] = []
ro_header_open_date_list : list[datetime.date] = []
ro_header_close_date_list : list[datetime.date] = []
ro_header_process_date_list : list[datetime.date] = []
ro_header_skip_flag_list : list[str] = []
ro_header_vin_list : list[str] = []
ro_header_customer_flag_list : list[str] = []
ro_header_customer_first_name_list : list[str] = []
ro_header_customer_last_name_list : list[str] = []
ro_header_customer_address_1_list : list[str] = []
ro_header_customer_address_2_list : list[str] = []
ro_header_customer_city_list : list[str] = []
ro_header_customer_state_list : list[str] = []
ro_header_customer_zip_list : list[str] = []
ro_header_customer_country_list : list = []
ro_header_customer_home_phone_list : list[str] = []
ro_header_customer_work_phone_list : list[str] = []
ro_header_customer_cell_phone_list : list[str] = []
ro_header_customer_sms_phone_list : list[str] = []
ro_header_customer_mms_phone_list : list[str] = []
ro_header_customer_email_list : list[str] = []
ro_header_service_advisor_code_list : list[str] = []
ro_header_customer_type_list : list[str] = []
ro_header_derived_customer_type_list : list[str] = []
ro_header_odometer_reading_list : list[int] = []
ro_header_odometer_code_list : list[str] = []
ro_header_customer_paid_part_amount_list : list[float] = []
ro_header_customer_paid_labour_amount_list : list[float] = []
ro_header_customer_paid_misc_amount_list : list[float] = []
ro_header_customer_paid_tax_amount_list : list[float] = []
ro_header_customer_paid_net_amount_list : list[float] = []
ro_header_total_part_amount_list : list[float] = []
ro_header_total_labour_amount_list : list[float] = []
ro_header_total_misc_amount_list : list[float] = []
ro_header_total_tax_amount_list : list[float] = []
ro_header_total_net_amount_list : list[float] = []

ro_labour_country_list: list[str] = []
ro_labour_dealer_list: list[str] = []
ro_labour_dealer_sub_code_list: list[str] = []
ro_labour_ro_list : list[str] = []
ro_labour_open_date_list : list[datetime.date] = []
ro_labour_close_date_list : list[datetime.date] = []
ro_labour_process_date_list : list[datetime.date] = []
ro_labour_skip_flag_list : list[str] = []
ro_labour_service_job_number_list  : list[int] = []
ro_labour_service_sequence_number_list  : list[int] = []
ro_labour_original_repair_type_code_list : list[str] = []
ro_labour_derived_repair_type_code_list : list[str] = []
ro_labour_react_category_code_list : list[str] = []
ro_labour_original_labour_op_code_list : list[str] = []
ro_labour_standard_labour_op_code_list : list[str] = []
ro_labour_service_hours_list : list[float] = []
ro_labour_customer_paid_labour_amount_list : list[float] = []


ro_part_country_list: list[str] = []
ro_part_dealer_list: list[str] = []
ro_part_dealer_sub_code_list: list[str] = []
ro_part_ro_list : list[str] = []
ro_part_open_date_list : list[datetime.date] = []
ro_part_close_date_list : list[datetime.date] = []
ro_part_process_date_list : list[datetime.date] = []
ro_part_skip_flag_list : list[str] = []
ro_part_service_job_number_list  : list[int] = []
ro_part_service_sequence_number_list  : list[int] = []
ro_part_part_sequence_number_list  : list[int] = []
ro_part_packed_part_code_list : list[str] = []
ro_part_customer_paid_part_amount_list : list[float] = []

for i in range(num_rows):
  country= random.choice(country_list)
  ro_header_country_list.append(country)
  dealer = random.randint(1000, 9999)
  ro_header_dealer_list.append(f"0{dealer}" if country == 'USA' else f"A{dealer}")
  ro_header_dealer_sub_code_list.append("")

  ro_header_ro_list.append(f"{random.randint(0, 999999999):016d}")
  ro_header_open_date_list.append(fake.date_between(start_date, end_date))
  ro_close_date = fake.date_between(ro_header_open_date_list[i], 
                        ro_header_open_date_list[i] + timedelta(days=random.randint(0,3)))
  ro_header_close_date_list.append(ro_close_date)
  ro_header_process_date_list.append(ro_close_date)

  ro_header_skip_flag_list.append('Y' if random.randint(1,101)%100 ==0 else '')
  ro_header_vin_list.append(fake.vin())

  ro_header_customer_flag_list.append('O' if random.randint(1,9)%8 == 0 else 'I')
  ro_header_customer_first_name_list.append(fake.first_name() 
                        if ro_header_customer_flag_list[i] == 'I' else "" )
  ro_header_customer_last_name_list.append(fake.last_name() 
                        if ro_header_customer_flag_list[i] == 'I' else fake.company() )
  ro_header_customer_address_1_list.append(fake.street_address() )
  ro_header_customer_address_2_list.append(fake.building_number() )
  ro_header_customer_city_list.append(fake.city() )
  ro_header_customer_state_list.append(fake.state() )
  ro_header_customer_zip_list.append(fake.zipcode() )
  ro_header_customer_country_list.append(country )

  ro_header_customer_home_phone_list.append(fake.phone_number() 
                        if random.randint(1,8) % 7 ==0 else "" )
  ro_header_customer_work_phone_list.append(fake.phone_number() 
                        if random.randint(1,8) % 7 ==0 else "" )
  ro_header_customer_cell_phone_list.append(fake.phone_number() )
  ro_header_customer_sms_phone_list.append(ro_header_customer_cell_phone_list[i] if i%6 ==0 else "" )
  ro_header_customer_mms_phone_list.append(ro_header_customer_cell_phone_list[i] if i%8 ==0 else "" )

  ro_header_customer_email_list.append( fake.email())

  ro_header_service_advisor_code_list.append(fake.ssn())

  customer_type = random.choice(list(cust_type_dict.keys()))
  ro_header_customer_type_list.append(customer_type)
  ro_header_derived_customer_type_list.append(cust_type_dict[customer_type])
  ro_header_odometer_reading_list.append(random.randint(0,99999))
  ro_header_odometer_code_list.append('K' if country == 'CAN' else 'M')

  customer_paid_part_amount : float = 0.0 # calculate later
  customer_paid_labour_amount : float = 0.0 # calculate later


  for j in range(1, (generate_labor_number()+1)):

    for k in range(1, (generate_labor_service_number()+1)):

      ro_labour_country_list.append(country)
      ro_labour_dealer_list.append(ro_header_dealer_list[i])
      ro_labour_dealer_sub_code_list.append("")
      ro_labour_ro_list.append(ro_header_ro_list[i])
      ro_labour_open_date_list.append(ro_header_open_date_list[i])
      ro_labour_close_date_list.append(ro_header_close_date_list[i])
      ro_labour_process_date_list.append(ro_header_process_date_list[i])
      ro_labour_skip_flag_list.append(ro_header_skip_flag_list[i])

      ro_labour_service_job_number_list.append(j)
      ro_labour_service_sequence_number_list.append(k)

      repair_type = random.choice(list(repair_type_dict.keys()))
      ro_labour_original_repair_type_code_list.append(repair_type)
      ro_labour_derived_repair_type_code_list.append(repair_type_dict[repair_type])
      ro_labour_react_category_code_list.append(f"{random.randint(11, 20)}")

      labour_op_code = random.choice(list(labour_op_code_dict.keys()))
      ro_labour_standard_labour_op_code_list.append(labour_op_code)
      ro_labour_original_labour_op_code_list.append(labour_op_code_dict.get(labour_op_code))
      ro_labour_service_hours_list.append(round(random.uniform(0.1, 4.0), 1))

      labor_amount : float = round(random.uniform(0, 10.0), 2)
      ro_labour_customer_paid_labour_amount_list.append(labor_amount)
      customer_paid_part_amount += labor_amount

      for l in range(1, (generate_part_number()+1)):

        ro_part_country_list.append(country)
        ro_part_dealer_list.append(ro_header_dealer_list[i])
        ro_part_dealer_sub_code_list.append("")
        ro_part_ro_list.append(ro_header_ro_list[i])
        ro_part_open_date_list.append(ro_header_open_date_list[i])
        ro_part_close_date_list.append(ro_header_close_date_list[i])
        ro_part_process_date_list.append(ro_header_process_date_list[i])
        ro_part_skip_flag_list.append(ro_header_skip_flag_list[i])

        ro_part_service_job_number_list.append(j)
        ro_part_service_sequence_number_list.append(k)
        ro_part_part_sequence_number_list.append(l)

        ro_part_packed_part_code_list.append(random.choice(packed_part_code_list))
        ro_part_customer_paid_part_amount_list.append(round(random.uniform(0, 10.0), 2))
        customer_paid_part_amount += ro_part_customer_paid_part_amount_list[l-1]

      customer_paid_labour_amount += round(random.uniform(0, 10.0), 2)

  customer_paid_misc_amount : float = round(random.uniform(0, 10.0), 2)
  customer_paid_tax_amount : float = round((customer_paid_part_amount + customer_paid_labour_amount 
                        + customer_paid_misc_amount) / random.choice([2,5,10]), 2)
  customer_paid_net_amount : float = round(((customer_paid_part_amount + customer_paid_labour_amount 
                        + customer_paid_misc_amount) + customer_paid_tax_amount), 2)

  total_part_amount: float = round(random.uniform(customer_paid_part_amount, 
                        customer_paid_part_amount * 2), 2)
  total_labour_amount : float = round(random.uniform(customer_paid_labour_amount, 
                        customer_paid_labour_amount * 2), 2)
  total_misc_amount : float = round(random.uniform(customer_paid_misc_amount, 
                        customer_paid_misc_amount * 2), 2)
  total_tax_amount : float = round(((total_part_amount + total_labour_amount + total_misc_amount) / 
                        random.choice([2,5,10])), 2)
  total_net_amount : float = round((total_part_amount + total_labour_amount + total_misc_amount + 
                        total_tax_amount), 2)

  ro_header_customer_paid_part_amount_list.append(round(customer_paid_part_amount,2))
  ro_header_customer_paid_labour_amount_list.append(customer_paid_labour_amount)
  ro_header_customer_paid_misc_amount_list.append(customer_paid_misc_amount)
  ro_header_customer_paid_tax_amount_list.append(customer_paid_tax_amount)
  ro_header_customer_paid_net_amount_list.append(customer_paid_net_amount)
  ro_header_total_part_amount_list.append(total_part_amount)
  ro_header_total_labour_amount_list.append(total_labour_amount)
  ro_header_total_misc_amount_list.append(total_misc_amount)
  ro_header_total_tax_amount_list.append(total_tax_amount)
  ro_header_total_net_amount_list.append(total_net_amount)

print(len(ro_header_country_list))
print(len(ro_header_dealer_list))
print(len(ro_header_dealer_sub_code_list))
print(len(ro_header_ro_list))
print(len(ro_header_open_date_list))
print(len(ro_header_close_date_list))
print(len(ro_header_process_date_list))
print(len(ro_header_skip_flag_list))
print(len(ro_header_vin_list))
print(len(ro_header_customer_flag_list))
print(len(ro_header_customer_first_name_list))
print(len(ro_header_customer_last_name_list))
print(len(ro_header_customer_address_1_list))
print(len(ro_header_customer_address_2_list))
print(len(ro_header_customer_city_list))
print(len(ro_header_customer_state_list))
print(len(ro_header_customer_zip_list))
print(len(ro_header_customer_country_list))
print(len(ro_header_customer_home_phone_list))
print(len(ro_header_customer_work_phone_list))
print(len(ro_header_customer_cell_phone_list))
print(len(ro_header_customer_sms_phone_list))
print(len(ro_header_customer_mms_phone_list))
print(len(ro_header_customer_email_list))
print(len(ro_header_service_advisor_code_list))
print(len(ro_header_customer_type_list))
print(len(ro_header_derived_customer_type_list))
print(len(ro_header_odometer_reading_list))
print(len(ro_header_odometer_code_list))
print(len(ro_header_customer_paid_part_amount_list))
print(len(ro_header_customer_paid_labour_amount_list))
print(len(ro_header_customer_paid_misc_amount_list))
print(len(ro_header_customer_paid_tax_amount_list))
print(len(ro_header_customer_paid_net_amount_list))
print(len(ro_header_total_part_amount_list))
print(len(ro_header_total_labour_amount_list))
print(len(ro_header_total_misc_amount_list))
print(len(ro_header_total_tax_amount_list))
print(len(ro_header_total_net_amount_list))
print(len(ro_labour_country_list))
print(len(ro_labour_dealer_list))
print(len(ro_labour_dealer_sub_code_list))
print(len(ro_labour_ro_list))
print(len(ro_labour_open_date_list))
print(len(ro_labour_close_date_list))
print(len(ro_labour_process_date_list))
print(len(ro_labour_skip_flag_list))
print(len(ro_labour_service_job_number_list))
print(len(ro_labour_service_sequence_number_list))
print(len(ro_labour_original_repair_type_code_list))
print(len(ro_labour_derived_repair_type_code_list))
print(len(ro_labour_react_category_code_list))
print(len(ro_labour_original_labour_op_code_list))
print(len(ro_labour_standard_labour_op_code_list))
print(len(ro_labour_service_hours_list))
print(len(ro_labour_customer_paid_labour_amount_list))
print(len(ro_part_country_list))
print(len(ro_part_dealer_list))
print(len(ro_part_dealer_sub_code_list))
print(len(ro_part_ro_list))
print(len(ro_part_open_date_list))
print(len(ro_part_close_date_list))
print(len(ro_part_process_date_list))
print(len(ro_part_skip_flag_list))
print(len(ro_part_service_job_number_list))
print(len(ro_part_service_sequence_number_list))
print(len(ro_part_packed_part_code_list))
print(len(ro_part_customer_paid_part_amount_list))

ro_header_data = {
    'country_code' : ro_header_country_list,
    'dealer_code' : ro_header_dealer_list,
    'dealer_sub_code' : ro_header_dealer_sub_code_list,
    'ro_number' : ro_header_ro_list,
    'ro_open_date' : ro_header_open_date_list,
    'ro_close_date' : ro_header_close_date_list,
    'ro_process_date' : ro_header_process_date_list,
    'skip_flag' : ro_header_skip_flag_list,
    'vin' : ro_header_vin_list,
    'customer_flag' : ro_header_customer_flag_list,
    'customer_first_name' : ro_header_customer_first_name_list,
    'customer_last_name' : ro_header_customer_last_name_list,
    'customer_address_1' : ro_header_customer_address_1_list,
    'customer_address_2' : ro_header_customer_address_2_list,
    'customer_city' : ro_header_customer_city_list,
    'customer_state' : ro_header_customer_state_list,
    'customer_zip' : ro_header_customer_zip_list,
    'customer_country' : ro_header_customer_country_list,
    'customer_home_phone' : ro_header_customer_home_phone_list,
    'customer_work_phone' : ro_header_customer_work_phone_list,
    'customer_cell_phone' : ro_header_customer_cell_phone_list,
    'customer_sms_phone' : ro_header_customer_sms_phone_list,
    'customer_mms_phone' : ro_header_customer_mms_phone_list,
    'customer_email' : ro_header_customer_email_list,
    'service_advisor_code' : ro_header_service_advisor_code_list,
    'customer_type' : ro_header_customer_type_list,
    'derived_customer_type' : ro_header_derived_customer_type_list,
    'odometer_reading' : ro_header_odometer_reading_list,
    'odometer_code' : ro_header_odometer_code_list,
    'customer_paid_part_amount' : ro_header_customer_paid_part_amount_list,
    'customer_paid_labour_amount' : ro_header_customer_paid_labour_amount_list,
    'customer_paid_misc_amount' : ro_header_customer_paid_misc_amount_list,
    'customer_paid_tax_amount' : ro_header_customer_paid_tax_amount_list,
    'customer_paid_net_amount' : ro_header_customer_paid_net_amount_list,
    'total_part_amount' : ro_header_total_part_amount_list,
    'total_labour_amount' : ro_header_total_labour_amount_list,
    'total_misc_amount' : ro_header_total_misc_amount_list,
    'total_tax_amount' : ro_header_total_tax_amount_list,
    'total_net_amount' : ro_header_total_net_amount_list
}

ro_labour_data = {
    'country_code' : ro_labour_country_list,
    'dealer_code' : ro_labour_dealer_list,
    'dealer_sub_code' : ro_labour_dealer_sub_code_list,
    'ro_number' : ro_labour_ro_list,
    'ro_open_date' : ro_labour_open_date_list,
    'ro_close_date' : ro_labour_close_date_list,
    'ro_process_date' : ro_labour_process_date_list,
    'skip_flag' : ro_labour_skip_flag_list,
    'service_job_number' : ro_labour_service_job_number_list,
    'service_sequence_number' : ro_labour_service_sequence_number_list,
    'original_repair_type_code' : ro_labour_original_repair_type_code_list,
    'derived_repair_type_code' : ro_labour_derived_repair_type_code_list,
    'react_category_code' : ro_labour_react_category_code_list,
    'original_labour_op_code' : ro_labour_original_labour_op_code_list,
    'standard_labour_op_code' : ro_labour_standard_labour_op_code_list,
    'service_hours' : ro_labour_service_hours_list,
    'customer_paid_labour_amount' : ro_labour_customer_paid_labour_amount_list
}

ro_part_data = {
    'country_code' : ro_part_country_list,
    'dealer_code' : ro_part_dealer_list,
    'dealer_sub_code' : ro_part_dealer_sub_code_list,
    'ro_number' : ro_part_ro_list,
    'ro_open_date' : ro_part_open_date_list,
    'ro_close_date' : ro_part_close_date_list,
    'ro_process_date' : ro_part_process_date_list,
    'skip_flag' : ro_part_skip_flag_list,
    'service_job_number' : ro_part_service_job_number_list,
    'service_sequence_number' : ro_part_service_sequence_number_list,
    'part_sequence_number' : ro_part_part_sequence_number_list,
    'packed_part_code' : ro_part_packed_part_code_list,
    'customer_paid_part_amount' : ro_part_customer_paid_part_amount_list
}

ro_header_df = pd.DataFrame(ro_header_data)
ro_labour_df = pd.DataFrame(ro_labour_data)
ro_part_df = pd.DataFrame(ro_part_data)

ro_header_df = ro_header_df.astype({"country_code": "string", "dealer_code": "string", 
                "dealer_sub_code": "string", "ro_number": "string", "ro_open_date" : "string", 
                "ro_close_date" : "string", "ro_process_date" : "string", "skip_flag": "string", 
                "vin": "string", "customer_flag": "string", "customer_first_name": "string", 
                "customer_last_name": "string", "customer_address_1": "string", 
                "customer_address_2": "string", "customer_city": "string", 
                "customer_state": "string", "customer_zip": "string", "customer_country": "string", 
                "customer_home_phone": "string", "customer_work_phone": "string", 
                "customer_cell_phone": "string", "customer_sms_phone": "string", 
                "customer_mms_phone": "string", "customer_email": "string", 
                "service_advisor_code": "string", "customer_type": "string", 
                "derived_customer_type": "string", "odometer_code": "string"})


ro_labour_df = ro_labour_df.astype({"country_code": "string", "dealer_code": "string",
                "dealer_sub_code": "string", "ro_number": "string", "ro_open_date" : "string", 
                "ro_close_date" : "string", "ro_process_date" : "string",
                "skip_flag" : "string", "original_repair_type_code": "string",
                "derived_repair_type_code": "string", "react_category_code": "string", 
                "original_labour_op_code": "string", "standard_labour_op_code": "string"})

ro_part_df = ro_part_df.astype({"country_code": "string","dealer_code": "string",
                "dealer_sub_code": "string", "ro_number" : "string", "ro_open_date" : "string", 
                "ro_close_date" : "string", "ro_process_date" : "string",
                "skip_flag": "string", "packed_part_code": "string"})


print(ro_header_df.info())
print(ro_labour_df.info())
print(ro_part_df.info())

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

ro_header_df.to_json(f"BQConversationalAgent/Data/Header/ro_header_{timestamp}.json", index=False,
                     orient='records', lines=True)
ro_labour_df.to_json(f"BQConversationalAgent/Data/Labour/ro_labour_{timestamp}.json", index=False,
                     orient='records', lines=True)
ro_part_df.to_json(f"BQConversationalAgent/Data/Part/ro_part_{timestamp}.json", index=False,
                   orient='records', lines=True)