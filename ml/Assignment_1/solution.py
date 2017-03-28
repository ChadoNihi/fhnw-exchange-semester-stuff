def load_data(need_printing = False):
    import csv

    #print('TASK 1. Load and visualize the dataset house_data.csv.\n')
    rows = []
    with open('house_data.csv', newline='') as fl:
        reader = csv.DictReader(fl, dialect='excel', delimiter=',', quoting=csv.QUOTE_NONE)

        if need_printing:
            for row in reader:
                print(row)
                rows.append(row)
        else
            for row in reader:
                rows.append(row)

    print('%d data entries has been read.\n' % len(rows))

def fname(arg):
    pass

if __name__ == '__main__':
    from sys import argv

    num_argv = len(argv)
