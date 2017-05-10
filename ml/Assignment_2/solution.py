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

    classify(points_for_each_class, print_stats=True)

def task_3(n_data_sets=10, n_points_cl_0=90, n_points_cl_1=100):
    print('TASK 3\n')

    data_sets, all_stats_noreg, all_stats_reg = [], [], []
    mean_x_cl_1 = 4.5
    d_mean_x_cl_1 = mean_x_cl_1 / n_data_sets
    # l=0
    for i in range(n_data_sets):
        data_sets.append(gen_data([(0.0,0.0), (mean_x_cl_1, 0.0)], [(1.0, 1.0), (1.0, 1.0)],
                                    [n_points_cl_0, n_points_cl_1]))
        all_stats_reg.append(classify(data_sets[i]))
        mean_x_cl_1 += d_mean_x_cl_1

    # l=10
    for data_set in data_sets:
        all_stats_noreg.append(classify(data_set, l=10))

    # display mean stats
    sum_acc, sum_prec, sum_rec, sum_f1 = 0, 0, 0, 0
    for stats in all_stats_noreg:
        sum_acc += stats['acc']
        sum_prec += stats['prec']
        sum_rec += stats['rec']
        sum_f1 += stats['f1']
    print('\nmean non-reg Accuracy: %.4f' % (sum_acc / n_data_sets))
    print('mean non-reg Precision: %.4f' % (sum_prec / n_data_sets))
    print('mean non-reg Recall: %.4f' % (sum_rec / n_data_sets))
    print('mean non-reg F1 score: %.4f' % (sum_f1 / n_data_sets))

    sum_acc, sum_prec, sum_rec, sum_f1 = 0, 0, 0, 0
    for stats in all_stats_reg:
        sum_acc += stats['acc']
        sum_prec += stats['prec']
        sum_rec += stats['rec']
        sum_f1 += stats['f1']
    print('\nmean reg Accuracy: %.4f' % (sum_acc / n_data_sets))
    print('mean reg Precision: %.4f' % (sum_prec / n_data_sets))
    print('mean reg Recall: %.4f' % (sum_rec / n_data_sets))
    print('mean reg F1 score: %.4f' % (sum_f1 / n_data_sets))


# LOGISTIC REG. FUNCTIONS
# (following Stanford's ML MOOC (https://www.coursera.org/learn/machine-learning/home)
#            and http://www.johnwittenauer.net/machine-learning-exercises-in-python-part-3/)

def cost(T, X, Y, l):
    T = np.matrix(T)
    X = np.matrix(X)
    Y = np.matrix(Y)

    lenX = len(X)

    reg = (l / 2 * lenX) * np.sum(np.power(T[:,1:T.shape[1]], 2))
    return np.sum( np.multiply(-Y, np.log(lr_h(T, X)))
                    - np.multiply((1-Y), np.log(1 - lr_h(T, X))) ) / lenX + reg

def grad_step(T, X, Y, l):
    T = np.matrix(T)
    X = np.matrix(X)
    Y = np.matrix(Y)

    n = T.ravel().shape[1]

    grad = np.zeros(n)
    err = lr_h(T, X) - Y

    lenX = len(X)
    grad[0] = np.sum(np.multiply(err, X[:,0])) / lenX
    for i in range(1, n):
        grad[i] = np.sum(np.multiply(err, X[:,i])) / lenX + (l / lenX)*T[:,i]

    return grad

def h(T, X):
    return np.dot(X, T.T)

def lr_h(T, X):
    return sig(h(T,X))

def optimise_T(T, X, Y, l):
    return opt.fmin_tnc(func=cost, x0=T, fprime=grad_step, args=(X, Y, l))

def predict(T, X, l):
    T = np.matrix(T)

    P = lr_h(T, X)
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

    return 0 if acc==0 and rec==0 else 2*acc*rec / (acc+rec)

def calc_precision(pred_Y, Y):
    m = len(pred_Y)
    if m != Y.size: raise ValueError('Error: pred_Y and Y should be of the same length.')

    tp, fp = 0, 0
    for i in range(m):
        if pred_Y[i] == 1 and Y.item(i) == 1:
            tp += 1
        elif pred_Y[i] == 1 and Y.item(i) == 0:
            fp += 1

    return 0 if tp==0 and fp==0 else tp / (tp+fp)

def calc_recall(pred_Y, Y):
    m = len(pred_Y)
    if m != Y.size: raise ValueError('Error: pred_Y and Y should be of the same length.')

    tp, p = 0, 0
    for i in range(m):
        if pred_Y[i] == 1 and Y.item(i) == 1:
            tp += 1
        if Y.item(i) == 1:
            p += 1

    return 0 if p==0 else tp / p


def classify(points_for_each_class, l=0, print_stats=False):
    len_0 = len(points_for_each_class[0])
    len_1 = len(points_for_each_class[1])

    X = np.c_[np.ones(len_0+len_1), np.concatenate([points_for_each_class[0], points_for_each_class[1]])]
    # 1 means 'belongs to class 0'
    Y = np.concatenate([np.ones(len_0), np.zeros(len_1)])
    T = optimise_T(np.zeros(len(points_for_each_class[0][0])+1), X, Y, l)[0]

    pred_Y = predict(T, X, l)

    stats = {'acc': calc_accuracy(pred_Y, Y),
            'prec': calc_precision(pred_Y, Y),
            'rec': calc_recall(pred_Y, Y),
            'f1': calc_F1(pred_Y, Y)}

    if print_stats:
        print('Predicted classification:')
        print(pred_Y)
        print('True classification:')
        print(Y)

        print('\nAccuracy: %.4f' % stats['acc'])
        print('Precision: %.4f' % stats['prec'])
        print('Recall: %.4f' % stats['rec'])
        print('F1 score: %.4f' % stats['f1'])

    return stats

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
    task_3()
