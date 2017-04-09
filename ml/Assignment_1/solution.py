import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

plt.figure(figsize=(8,6))

def task_1():
    print('TASK 1. Load and visualize the dataset house_data.csv.\n')
    load_data(True)

def task_2(rows, skip_graps=False):
    print('\nTASK 2')

    lr = linear_model.LinearRegression()
    X = np.array([[row['sqft_living']] for row in rows]) #.astype(np.float)
    y = np.array([row['price'] for row in rows]) #.astype(np.float)

    lr.fit(X, y)
    predicted_y = lr.predict(X)

    plt.scatter(X, y,  color='black', s=3)
    plt.plot(X, predicted_y, color='blue', linewidth=3)

    plt.xlabel('sqft_living', fontsize=14)
    plt.ylabel('price', fontsize=14)

    plt.tight_layout()
    if skip_graps:
        plt.clf()
    else:
        plt.show()

    # now the Tukey-Anscombe plot
    plt.scatter(predicted_y, y-predicted_y,  color='black', s=3)
    plt.axhline(linewidth=2, color='black')

    plt.title('the Tukey-Anscombe plot, task 2')
    plt.xlabel('predicted_y', fontsize=14)
    plt.ylabel('r', fontsize=14)
    plt.figtext(.02, .01, 'The \'left arrow\' shape\nindicates a linear increase of\nstandard deviation with the fitted values')

    plt.tight_layout()
    if skip_graps:
        plt.clf()
    else:
        plt.show()

    return {'y': y, 'predicted_y': predicted_y}

def task_3(rows, skip_graps=False):
    from math import sqrt

    print('\nTASK 3')

    lr = linear_model.LinearRegression()
    X = np.array([[row['sqft_living']] for row in rows]) #.astype(np.float)
    log_y = np.log([row['price'] for row in rows])

    lr.fit(X, log_y)
    predicted_y = lr.predict(X)
    residuals = log_y-predicted_y

    plt.scatter(X, log_y,  color='black', s=3)
    plt.plot(X, predicted_y, color='blue', linewidth=3)

    plt.xlabel('sqft_living', fontsize=14)
    plt.ylabel('log_price', fontsize=14)

    plt.tight_layout()
    if skip_graps:
        plt.clf()
    else:
        plt.show()

    # now the Tukey-Anscombe plot
    plt.scatter(predicted_y, residuals,  color='black', s=3)
    plt.axhline(linewidth=2, color='black')

    plt.title('the Tukey-Anscombe plot, task 3')
    plt.xlabel('predicted_y', fontsize=14)
    plt.ylabel('r', fontsize=14)
    plt.figtext(.02, .01, 'With the transformation Y -> log(Y)\nthe residuals seem to be closer\nto a constant variability.')

    plt.tight_layout()
    if skip_graps:
        plt.clf()
    else:
        plt.show()

    # histogram of the residuals
    n_bins = 100
    plt.hist(residuals, n_bins)

    plt.title('A histogram of the residuals, task 3')
    plt.ylabel('predicted_y - log_y', fontsize=14)

    if skip_graps:
        plt.clf()
    else:
        plt.show()

    variance = np.var(residuals)
    print('Variance of the residuals: %f' % variance)
    print('SD of the residuals: %f' % sqrt(variance))

    return {'log_y': log_y, 'predicted_y': predicted_y}

def task_4(res_task2, res_task3):
    print('\nTASK 4')

    print('MAPE: %f' % get_mape(res_task3['log_y'], res_task3['predicted_y']))
    print('MdAPE: %f' % get_mdape(res_task3['log_y'], res_task3['predicted_y']))

    n_bins = 100

    apes = np.abs((res_task2['y'] - res_task2['predicted_y']) / res_task2['y'])
    plt.hist(apes, n_bins)

    plt.title('A histogram of the task_2\'s APEs, task 4')
    plt.ylabel('error', fontsize=14)

    plt.show()

    # repeat for the task 3 data
    apes = np.abs((res_task3['log_y'] - res_task3['predicted_y']) / res_task3['log_y'])
    plt.hist(apes, n_bins)

    plt.title('A histogram of the task_3\'s APEs, task 4')
    plt.ylabel('error', fontsize=14)

    plt.show()

def task_5(rows):
    from math import inf
    from matplotlib.cm import ScalarMappable

    print('\nTASK 5')

    clrmap = ScalarMappable()

    min_pr, max_pr = inf, -inf
    for row in rows:
        pr = row['price']
        if pr > max_pr:
            max_pr = pr
        elif pr < min_pr:
            min_pr = pr

    longs, lats, zcodes, szs = zip(*[(row['lat'], row['long'],
                                row['zipcode'],
                                np.interp(row['price'], [min_pr, max_pr], [1,50])**2) for row in rows])

    plt.scatter(longs, lats,  c=zcodes, cmap=plt.cm.coolwarm, s=szs, alpha=0.4)

    plt.title('The spatial distribution of ‘zipcode‘ (color) and ‘price‘ (size), task 5')
    plt.xlabel('long', fontsize=14)
    plt.ylabel('lat', fontsize=14)

    plt.tight_layout()
    print('The high-price houses tend to be close to other pricy houses.')
    plt.show()

def task_6(rows, skip_graps=False):

    print('\nTASK 6')

    lr = linear_model.LinearRegression()
    X = np.array([[row['sqft_living'], row['zipcode']] for row in rows]) #.astype(np.float)
    log_y = np.log([row['price'] for row in rows])

    lr.fit(X, log_y)
    predicted_y = lr.predict(X)
    residuals = log_y-predicted_y

    plt.scatter(predicted_y, residuals,  color='black', s=3)
    plt.axhline(linewidth=2, color='black')

    plt.title('the Tukey-Anscombe plot, task 6')
    plt.xlabel('predicted_y', fontsize=14)
    plt.ylabel('r', fontsize=14)

    plt.tight_layout()
    if skip_graps:
        plt.clf()
    else:
        plt.show()

    n_bins = 100
    plt.hist(residuals, n_bins)

    plt.title('A histogram of the residuals, task 6')
    plt.ylabel('predicted_y - log_y', fontsize=14)

    if skip_graps:
        plt.clf()
    else:
        plt.show()

    print('MAPE: %f' % get_mape(log_y, predicted_y))
    print('MdAPE: %f' % get_mdape(log_y, predicted_y))

    print('Adding "zipcode" feature to the model made little difference to the results.')

def task_7(rows, skip_graps=False):

    print('\nTASK 7')

    lr = linear_model.LinearRegression()
    X = np.array([[row['sqft_living'], row['zipcode'], row['bedrooms'],
                    row['bathrooms'], row['grade'], row['yr_built']] for row in rows]) #.astype(np.float)
    log_y = np.log([row['price'] for row in rows])

    lr.fit(X, log_y)
    predicted_y = lr.predict(X)
    residuals = log_y-predicted_y

    plt.scatter(predicted_y, residuals,  color='black', s=3)
    plt.axhline(linewidth=2, color='black')

    plt.title('the Tukey-Anscombe plot, task 7')
    plt.xlabel('predicted_y', fontsize=14)
    plt.ylabel('r', fontsize=14)

    plt.tight_layout()
    if skip_graps:
        plt.clf()
    else:
        plt.show()

    n_bins = 100
    plt.hist(residuals, n_bins)

    plt.title('A histogram of the residuals, task 7')
    plt.ylabel('predicted_y - log_y', fontsize=14)

    if skip_graps:
        plt.clf()
    else:
        plt.show()

    MAPE = get_mape(log_y, predicted_y)
    MdAPE = get_mdape(log_y, predicted_y)
    print('MAPE: %f' % MAPE)
    print('MdAPE: %f' % MdAPE)

    print('Adding more features improved accuracy on the train dataset. MAPE & MdAPE are reduced.')

    return (lr.coef_, MAPE, MdAPE)

def task_8(rows, theta_task_7, MAPE_7, MdAPE_7): # since
    print('\nTASK 8')

    X = np.array([[row['sqft_living'], row['zipcode'], row['bedrooms'],
                    row['bathrooms'], row['grade'], row['yr_built']] for row in rows]) #.astype(np.float)
    log_y = np.log([row['price'] for row in rows])

    lamb_1, lamb_2 = 0, 10
    theta_1 = get_theta_lg(X, log_y, lamb_1)
    theta_2 = get_theta_lg(X, log_y, lamb_2)

    lr = linear_model.LinearRegression()

    print('thetas task 7: ', theta_task_7)
    print('MAPE: %f' % MAPE_7)
    print('MdAPE: %f' % MdAPE_7)

    predicted_y_1 = predict_from_theta(theta_1, X)
    print('\n\nthetas task 8, lambda = %f: ' % lamb_1, theta_1)
    print('MAPE: %f' % get_mape(log_y, predicted_y_1))
    print('MdAPE: %f' % get_mdape(log_y, predicted_y_1))

    predicted_y_2 = predict_from_theta(theta_2, X)
    print('\n\nthetas task 8, lambda = %f: ' % lamb_2, theta_2)
    print('MAPE: %f' % get_mape(log_y, predicted_y_2))
    print('MdAPE: %f' % get_mdape(log_y, predicted_y_2))

# HELPER FUNCTIONS
def get_theta_lg(X, y, lamb=0): # adopted from http://stackoverflow.com/questions/34170618/normal-equation-and-numpy-least-squares-solve-methods-difference-in-regress
    Isz = X.shape[1]
    Istar = np.zeros((Isz, Isz))
    np.fill_diagonal(Istar, 1)

    return np.linalg.lstsq(X.T.dot(X) + lamb * Istar, X.T.dot(y))[0]

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

    print('%d data entries have been read.\n' % len(rows))

    return rows

def get_mape(y, predicted_y):
    print(y[0], predicted_y[0])
    return np.mean(np.abs((y - predicted_y) / y))

def get_mdape(y, predicted_y):
    return np.median(np.abs((y - predicted_y) / y))

def predict_from_theta(theta, X):
    return [sum( [th*x for th, x in zip(theta, x_row)] ) for x_row in X]

def preprocess_data(raw_rows):
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

        rows.append(row)

    return rows

if __name__ == '__main__':
    rows = preprocess_data(load_data())

    task_8(rows, *task_7(rows, True))
