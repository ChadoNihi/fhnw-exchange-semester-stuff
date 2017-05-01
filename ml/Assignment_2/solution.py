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


# LOGISTIC REG. FUNCTIONS
# (following Stanford's ML MOOC (https://www.coursera.org/learn/machine-learning/home)
#            and http://www.johnwittenauer.net/machine-learning-exercises-in-python-part-3/)

def cost(X, Y, T, l = 0):
    reg = (l / 2 * len(X)) * np.sum(np.power(T[:,1:T.shape[1]], 2))
    return np.sum( np.multiply(-Y, np.log(lr_h(X, T)))
                    - np.multiply((1-Y), np.log(1 - lr_h(X, T))) ) / len(X) + reg

def grad_step(T, X, Y, l):
    n = T.ravel().shape[1]

    grad = np.zeros(n)
    err = lr_h(X, T) - Y

    grad[0] = np.sum(np.multiply(err, X[:,0])) / len(X)
    for i in range(1, n):
        grad[i] = np.sum(np.multiply(err, X[:,i])) / len(X) + (l / len(X))*T[:,i]

    return grad

def h(X, T):
    return np.dot(X, T)

def lr_h(X, T):
    return sig(h(X,T))

def optimise_T(X, Y, T, l):
    return opt.fmin_tnc(func=cost, x0=T, fprime=grad_step, args=(X, Y, l))

def predict(X, Y, T, l):
    P = lr_h(X, optimise_T(X, Y, T, l)[0])
    return [1 if x >= 0.5 else 0 for x in P]

def sig(Z):
	return 1 / (1 + np.exp(-Z))

# HELPER FUNCTIONS

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
    task_1(data_task_1)
    task_2(data_task_1)
