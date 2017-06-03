import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt

def task_1():
    print('TASK 1\n')

    _process_loaded_data(_load_data())

def _load_data(need_printing = False):
    import csv

    rows = []
    with open('house_data.csv', newline='') as fl:
        reader = csv.DictReader(fl, dialect='excel', delimiter=',', quoting=csv.QUOTE_NONE)

        if need_printing:
            for row in reader:
                print(row)
                rows.append(row)
        else:
            for row in reader:
                rows.append(row)

    if need_printing: print('%d data entries have been read.\n' % len(rows))

    return rows

def _process_loaded_data(raw_rows):
    from datetime import datetime
    curr_y = datetime.today().year

    ks_of_quoted_vals = ['floors', 'zipcode', 'id', 'sqft_lot15']
    rows = []
    for row in raw_rows:
        for k,v in row.items():
            if k == 'date':
                continue
            elif k in ks_of_quoted_vals:
                row[k] = float(v.strip('"'))
            else:
                row[k] = float(v)

        row['yrs_since_modified'] = curr_y - (row['yr_renovated'] or row['yr_built'])
        rows.append(row)

    return rows

if __name__ == '__main__':
    task_1()
