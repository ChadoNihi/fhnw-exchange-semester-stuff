import numpy as np

def task_1():
    print('TASK 1. Load and visualize the dataset house_data.csv.\n')
    load_data(True)

def task_2(rows):
    import matplotlib.pyplot as plt
    from sklearn import linear_model

    lr = linear_model.LinearRegression()
    X = np.array([[row['sqft_living']] for row in rows]).astype(np.float)
    y = np.array([row['price'] for row in rows]).astype(np.float)

    lr.fit(X, y)
    predicted_y = lr.predict(X)

    plt.scatter(X, y,  color='black')
    plt.plot(X, predicted_y, color='blue', linewidth=3)

    plt.xlabel('sqft_living', fontsize=15)
    plt.ylabel('price', fontsize=15)

    plt.tight_layout()
    plt.show()

    # now the Tukey-Anscombe plot
    plt.scatter(y-predicted_y,  color='black')

# HELPER FUNCTIONS
def load_data(need_printing = False):
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

    print('%d data entries has been read.\n' % len(rows))

    return rows

if __name__ == '__main__':
    task_2(load_data())
