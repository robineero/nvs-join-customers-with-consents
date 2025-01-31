import sys
import csv
import datetime

if (len(sys.argv) < 2):
    print("ERROR: Please add customers and consents CSV files as arguments.\n")
    exit()

customers_csv = sys.argv[1].lstrip(".\\")
consents_csv = sys.argv[2].lstrip(".\\")
filetype = consents_csv.split(".")[-1]

if (filetype != "csv"):
    print("ERROR: File type must be csv but at the moment it is {}.".format(filetype))
    exit()

print("----\n")
print ("Customers:\t{}".format(customers_csv))
print ("Consents:\t{}".format(consents_csv))
print ("File type: {}".format(filetype))
print("----\n")


def get_unix_date(capture_datetime) -> int:
  
  return int(datetime.datetime.strptime(capture_datetime, "%m/%d/%Y %I:%M %p").timestamp())

def get_consents_dict(csv_file) -> dict:

    consents = {}

    with open(csv_file, encoding='utf-8') as csv_file:

        csv_reader = csv.reader(csv_file)
        header_set = False;

        for line in csv_reader:

            if (not header_set):
                consents["header"] = {'line': line}
                header_set = True
                continue

            salesforce_id = line[0]
            capture_datetime = line[6]
            opt_type = line[16]
            
            if (not capture_datetime): continue
            
            unix_int = get_unix_date(capture_datetime)

            if (not consents.get(salesforce_id)):
                consents[salesforce_id] = {'salesforce_id': salesforce_id, 'time': unix_int, 'opt_type': opt_type, 'line': line}
            else:
                if (consents.get(salesforce_id).get('time') < unix_int):
                    consents[salesforce_id] = {'salesforce_id': salesforce_id, 'time': unix_int, 'opt_type': opt_type, 'line': line}

    return consents


def get_customers_dict(csv_file) -> dict:

    customers = {}

    with open(csv_file, encoding='utf-8') as csv_file:

        csv_reader = csv.reader(csv_file)
        
        header_set = False;

        for line in csv_reader:
            if (not header_set):
                customers["header"] = {'line': line}
                header_set = True
                continue

            salesforce_id = line[1]
            customers[salesforce_id] = {'line': line}

    return customers


def join_customers_consents(customers, consents):

    current_time = datetime.datetime.now()
    current_current_string = current_time.strftime('%y%m%d-%H%M')
    filename = "customers_consents_%s.csv" % (current_current_string)

    with open(filename, "w", newline='', encoding='utf-8') as new_file:

        csv_writer = csv.writer(new_file)
        csv_writer.writerow(customers['header'].get('line') + consents['header'].get('line'))

        for key in customers:
            if (key == "header"): continue
            customer_consent = consents.get(key).get('line') if consents.get(key) else []
            csv_writer.writerow(customers[key].get('line') + customer_consent)

    return True


consents = get_consents_dict(consents_csv)
customers = get_customers_dict(customers_csv)
join_customers_consents(customers, consents)
