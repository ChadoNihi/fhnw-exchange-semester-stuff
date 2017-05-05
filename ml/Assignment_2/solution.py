from math import exp
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt

def task_1(points_for_each_class):
    print('TASK 1\n')

    plt.scatter(points_for_each_class[0][:,0], points_for_each_class[0][:,1],  color='blue', s=4)
    plt.scatter(points_for_each_class[1][:,0], points_for_each_class[1][:,1],  color='green', s=4)

    plt.xlabel('feature 1', fontsize=14)
    plt.ylabel('feature 2', fontsize=14)

    plt.tight_layout()
    plt.show()

def task_2(points_for_each_class):
    print('TASK 2\n')

    len_0 = len(points_for_each_class[0])
    len_1 = len(points_for_each_class[1])

    X = np.matrix(np.c_[np.ones(len_0+len_1), np.concatenate([points_for_each_class[0], points_for_each_class[1]])])
    # 1 means 'belongs to class 0'
    Y = np.matrix(np.concatenate([np.ones(len_0), np.zeros(len_1)]))
    T = np.matrix(np.zeros(len(points_for_each_class[0][0])+1))

    pred_Y = predict(X, T)

    print('Predicted classification:')
    print(pred_Y)
    print('True classification:')
    print(Y)

    print('\nAccuracy: %f' % calc_accuracy(pred_Y, Y))
    print('Precision: %f' % calc_precision(pred_Y, Y))
    print('Recall: %f' % calc_recall(pred_Y, Y))
    print('F1 score: %f' % calc_F1(pred_Y, Y))


# LOGISTIC REG. FUNCTIONS
# (following Stanford's ML MOOC (https://www.coursera.org/learn/machine-learning/home)
#            and http://www.johnwittenauer.net/machine-learning-exercises-in-python-part-3/)

def cost(X, Y, T, l=0):
    reg = (l / 2 * len(X)) * np.sum(np.power(T[:,1:T.shape[1]], 2))
    return np.sum( np.multiply(-Y, np.log(lr_h(X, T)))
                    - np.multiply((1-Y), np.log(1 - lr_h(X, T))) ) / len(X) + reg

def grad_step(T, X, Y, l=0):
    n = T.ravel().shape[1]

    grad = np.zeros(n)
    err = lr_h(X, T) - Y

    grad[0] = np.sum(np.multiply(err, X[:,0])) / len(X)
    for i in range(1, n):
        grad[i] = np.sum(np.multiply(err, X[:,i])) / len(X) + (l / len(X))*T[:,i]

    return grad

def h(X, T):
    return np.dot(X, T.T)

def lr_h(X, T):
    return sig(h(X,T))

def optimise_T(X, Y, T, l=0):
    return opt.fmin_tnc(func=cost, x0=T, fprime=grad_step, args=(X, Y, l))

def predict(X, T, l=0):
    P = lr_h(X, T)
    return [1 if x >= 0.5 else 0 for x in P]

def sig(Z):
	return 1 / (1 + np.exp(-Z))

# HELPER FUNCTIONS

def calc_accuracy(pred_Y, Y):
    m = len(pred_Y)
    if m != Y.size: raise ValueError('Error: pred_Y and Y should be of the same length.')

    n_right = 0
    for i in range(m):
        if pred_Y[i] == Y.item(i): n_right += 1

    return n_right / m

def calc_F1(pred_Y, Y):
    acc = calc_accuracy(pred_Y, Y)
    rec = calc_recall(pred_Y, Y)

    return 2*acc*rec / (acc+rec)

def calc_precision(pred_Y, Y):
    m = len(pred_Y)
    if m != Y.size: raise ValueError('Error: pred_Y and Y should be of the same length.')

    tp, fp = 0, 0
    for i in range(m):
        if pred_Y[i] == 1 and Y.item(i) == 1:
            tp += 1
        elif pred_Y[i] == 1 and Y.item(i) == 0:
            fp += 1

    return tp / (tp+fp)

def calc_recall(pred_Y, Y):
    m = len(pred_Y)
    if m != Y.size: raise ValueError('Error: pred_Y and Y should be of the same length.')

    tp, p = 0, 0
    for i in range(m):
        if pred_Y[i] == 1 and Y.item(i) == 1:
            tp += 1
        if Y.item(i) == 1:
            p += 1

    return tp / p



def gen_data(means, sdevs, n_points_per_class):
    from random import gauss

    n_classes = len(means)

    if not isinstance(n_points_per_class, list):
        n_points_per_class = [n_points_per_class] * n_classes

    return np.asarray([ [(gauss(means[class_i][0],sdevs[class_i][0]), gauss(means[class_i][1],sdevs[class_i][1]))
                                for _ in range(n_points_per_class[class_i])]
                for class_i in range(n_classes) ])


if __name__ == '__main__':
    data_task_1 = gen_data([(-4, 1), (2, 3)], [(1.2, 0.8), (0.7, 1)], 50)
    #task_1(data_task_1)
    task_2(data_task_1)
