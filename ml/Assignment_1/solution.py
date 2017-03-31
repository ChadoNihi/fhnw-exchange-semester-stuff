import numpy as np

def task_1():
    print('TASK 1. Load and visualize the dataset house_data.csv.\n')
    load_data(True)

def task_2(rows):
    import matplotlib.pyplot as plt
    from sklearn import linear_model

    print('TASK 2')

    lr = linear_model.LinearRegression()
    X = np.array([[row['sqft_living']] for row in rows]).astype(np.float)
    y = np.array([row['price'] for row in rows]).astype(np.float)

    lr.fit(X, y)
    predicted_y = lr.predict(X)

    plt.scatter(X, y,  color='black', s=3)
    plt.plot(X, predicted_y, color='blue', linewidth=3)

    plt.xlabel('sqft_living', fontsize=14)
    plt.ylabel('price', fontsize=14)

    plt.tight_layout()
    plt.show()

    # now the Tukey-Anscombe plot
    plt.scatter(predicted_y, y-predicted_y,  color='black', s=3)
    plt.axhline(linewidth=2, color='black')

    plt.title('the Tukey-Anscombe plot, task 2')
    plt.xlabel('predicted_y', fontsize=14)
    plt.ylabel('r', fontsize=14)
    plt.figtext(.02, .01, 'The \'left arrow\' shape\nindicates a linear increase of\nstandard deviation with the fitted values')

    plt.tight_layout()
    plt.show()

def task_3(rows):
    from math import log, sqrt
    import matplotlib.pyplot as plt
    from sklearn import linear_model

    print('TASK 3')

    lr = linear_model.LinearRegression()
    X = np.array([[row['sqft_living']] for row in rows]).astype(np.float)
    y = np.array([row['price'] for row in rows]).astype(np.float)

    lr.fit(X, y)
    log_predicted_y = np.log(lr.predict(X))
    residuals = y-log_predicted_y

    plt.scatter(X, y,  color='black', s=3)
    plt.plot(X, log_predicted_y, color='blue', linewidth=3)

    plt.xlabel('sqft_living', fontsize=14)
    plt.ylabel('price', fontsize=14)

    plt.tight_layout()
    plt.show()

    # now the Tukey-Anscombe plot
    plt.scatter(log_predicted_y, residuals,  color='black', s=3)
    plt.axhline(linewidth=2, color='black')

    plt.title('the Tukey-Anscombe plot, task 3')
    plt.xlabel('log_predicted_y', fontsize=14)
    plt.ylabel('r', fontsize=14)
    plt.figtext(.02, .01, 'With the transformation Y -> log(Y)\nthe residuals seem to be closer\nto a constant variability.')

    plt.tight_layout()
    plt.show()

    # histogram of the residuals
    n_bins = 100
    plt.hist(residuals, n_bins)

    plt.title('A histogram of the residuals, task 3')
    plt.ylabel('log_predicted_y - y', fontsize=14)

    plt.show()

    variance = np.var(residuals)
    print('Variance of the residuals: %f' % variance)
    print('SD of the residuals: %f' % sqrt(variance))

    #return {'y': }

def task_4(y, ):
    print('TASK 4')

    print('MAPE: %f' % get_mape())
    print('MdAPE: %f' % get_mdape())

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

def get_mape(y, predicted_y):
    return np.mean(np.abs((y - predicted_y) / y))

def get_mdape(y, predicted_y):
    return np.median(np.abs((y - predicted_y) / y))

if __name__ == '__main__':
    task_3(load_data())
