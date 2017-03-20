import csv
import datetime
import re

clean_data = []
clean_keys = None
with open('data/persons.csv', newline='') as f:
    clean_keys = next(csv.reader(f))
    clean_data.append(clean_keys)


with open('data/persons-raw.csv', newline='') as f:
    reader = csv.DictReader(f)
    re_date_key = re.compile(r'\bdate\b', re.I)

    for raw_row in reader:
        if not len(raw_row['Index']): continue

        clean_row = []

        for clean_key in clean_keys:
            if clean_key in raw_row:
                if re.search(re_date_key, clean_key):
                    date_str = None
                    try:
                        datetime.datetime.strptime(raw_row[clean_key], "%d.%m.%Y")
                        date_str = raw_row[clean_key]
                    except ValueError:
                        try:
                            date_str = datetime.datetime.strptime(raw_row[clean_key], "%d.%m.%y").date().strftime('%d.%m.%Y')
                        except ValueError:
                            date_str = ''
                    clean_row.append(date_str)

                else:
                    clean_row.append(raw_row[clean_key].capitalize())
            elif clean_key == 'Shirt Size':
                if raw_row['Small Shirt Size'] == 'X':
                    clean_row.append('S')
                elif raw_row['Medium Shirt Size'] == 'X':
                    clean_row.append('M')
                elif raw_row['Large Shirt Size'] == 'X':
                    clean_row.append('L')
                else:
                    clean_row.append('')
            else:
                clean_row.append('')

        clean_data.append(clean_row)

with open('data/persons-cooked.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(clean_data)
