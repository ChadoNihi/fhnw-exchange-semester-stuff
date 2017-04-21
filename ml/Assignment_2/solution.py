import matplotlib.pyplot as plt
import numpy as np

def task_1(points_for_each_class):
    print('TASK 1\n')

    plt.scatter(points_for_each_class[0][:,0], points_for_each_class[0][:,1],  color='blue', s=4)
    plt.scatter(points_for_each_class[1][:,0], points_for_each_class[1][:,1],  color='green', s=4)

    plt.xlabel('feature 1', fontsize=14)
    plt.ylabel('feature 2', fontsize=14)

    plt.tight_layout()
    plt.show()

def task_2(points_for_each_class):
    pass
    

# LOGISTIC REG. FUNCTIONS

def cost():
    pass

def h(arg):
    pass

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
