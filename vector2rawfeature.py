import numpy as np
import scipy.interpolate
names = ['mxy', 'xr', 'cxt']


def remove_ith(data, i):
    newData = []
    for d in data:
        if d[0] != i:
            newData.append(d)
    return np.array(newData)

def interp(data, N):
    intper = scipy.interpolate.interp1d()

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
    # print count
    # delete the samples with count less or equal than 40
    for i in range(0, len(count[0])):
        if count[0][i] <= 40:
            data = remove_ith(data, i + 1)
    newData = []
    lastIndex = 0
    count = -1
    for d in data:
        if d[0] != lastIndex:
            newData.append([])
            count += 1
            lastIndex = d[0]
        d[0] = count
        newData[count].append(d)
    newData = np.array(newData)
    # print newData
    np.save('raw_vector_' + name, newData)

