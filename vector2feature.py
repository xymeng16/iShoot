import numpy as np

names = ['mxy', 'xr', 'cxt']

for name in names:

    last_index = 0
    data = np.loadtxt(fname='vector_' + name + '.txt', dtype=int, usecols=[0, 2, 3, 4, 5, 6, 7])
    # print data[0]
    for i in range(0, len(data)):
        data[i][0] -= 1
    # print data[0]
    count = np.zeros((1, data[len(data) - 1][0]))
    # np.random.normal(size=(1, 6))
    for i in range(0, len(data)):
        count[0][data[i][0] - 1] += 1
    print count
    # delete the samples with count less or equal than 40
    toBeDeleted = []
    for i in range(0, len(count[0])):
        if count[0][i] <= 40:
            toBeDeleted.append()
    print toBeDeleted
def remove_ith():
