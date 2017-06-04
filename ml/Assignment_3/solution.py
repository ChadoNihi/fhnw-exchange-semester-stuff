import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

def task_1(n_components = 3):
    print('TASK 1\n')

    ds_1 = _form_sub_ds(_process_loaded_data(_load_data()))

    keys_in_fixed_order = ds_1[0].keys()
    X = [[row[k] for k in keys_in_fixed_order] for row in ds_1]

    pca = PCA(n_components = n_components)
    pca.fit(X)

    print(pca.components_)
    print('Percentage of variance explained:', pca.explained_variance_ratio_)
    print('Percentage of variance:', pca.explained_variance_)

    return ds_1

def task_2(ds_1, variance_threshold = 0.9):
    print('TASK 2\n')

    max_n_components = len(ds_1[0]) # == n of features in ds_1
    keys_in_fixed_order = ds_1[0].keys()

    ns = [n for n in range(1, max_n_components+1)]
    X = [[row[k] for k in keys_in_fixed_order] for row in ds_1]

    pca = PCA()
    pca.fit(X)

    cumsum = pca.explained_variance_ratio_.cumsum()
    print('Cumulative sums: ', cumsum)

    # drawing plot logic
    fig, ax = plt.subplots()
    bar_w = 0.5
    ax.bar(ns, cumsum, bar_w, color='b')

    ax.set_title('cumulative sum of the variance vs # of considered PCs')
    ax.set_xlabel('# of components')
    ax.set_ylabel('% variance')

    plt.show()

    # making DSc
    n_components_90var = 0
    for var in cumsum:
        if var < variance_threshold:
            n_components_90var += 1

    n_components_90var = max(n_components_90var, 1)

    pca = PCA(n_components_90var)

    return pca.fit_transform(X)

def _form_sub_ds(orig_ds,features=['price','sqft_living','sqft_lot','sqft_basement','sqft_above','yrs_since_modified','sqft_lot15','sqft_living15']):
    new_ds = []
    for row in orig_ds:
        new_ds.append( { ftr: row[ftr] for ftr in features } )

    return new_ds

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
    ds_1 = task_1()
    X_ds_c = task_2(ds_1)
