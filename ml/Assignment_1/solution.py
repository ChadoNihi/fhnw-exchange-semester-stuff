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

    return rows

def task_2(rows):
    lr = linear_model.LinearRegression(C = 1e12) #large C -> small lambda -> ~no regularization
    regr.fit(diabetes_X_train, diabetes_y_train)

    plt.scatter(diabetes_X_test, diabetes_y_test,  color='black')
    plt.plot(diabetes_X_test, lr.predict(diabetes_X_test), color='blue', linewidth=3)

    plt.xticks(())
    plt.yticks(())

    plt.show()

# HELPER FUNCTIONS

if __name__ == '__main__':
    from sys import argv

    num_argv = len(argv)
