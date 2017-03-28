import numpy as np
import matplotlib.pylab as plt
from scipy.interpolate import interp1d


# function for extrapolation
def extrap1d(interpolator):
    xs = interpolator.x
    ys = interpolator.y

    def pointwise(x):
        if x < xs[0]:
            return ys[0] + (x - xs[0]) * (ys[1] - ys[0]) / (xs[1] - xs[0])
        elif x > xs[-1]:
            return ys[-1] + (x - xs[-1]) * (ys[-1] - ys[-2]) / (xs[-1] - xs[-2])
        else:
            return interpolator(x)

    def ufunclike(xs):
        return np.array(map(pointwise, np.array(xs)))

    return ufunclike


# interpolate and compute the feature

data_mxy = np.load('raw_vector_mxy.npy')
data_cxt = np.load('raw_vector_cxt.npy')
data_xr = np.load('raw_vector_xr.npy')

maxCount = -1

findOne = False

for ds in data_mxy:
    if len(ds) > maxCount:
        maxCount = len(ds)
for ds in data_cxt:
    if len(ds) > maxCount:
        maxCount = len(ds)
for ds in data_xr:
    if len(ds) > maxCount:
        maxCount = len(ds)
print maxCount
feature_vectors = {'mxy': [], 'xr': [], 'cxt': []}

for idx in range(0, len(data_mxy)):
    d = np.array(data_mxy[idx])
    newData = []
    for i in range(1, 7):
        y = d[:, i]
        x = np.arange(0, len(y), 1)
        xNew = np.linspace(0, len(x), maxCount)
        # yNew = np.interp(xNew, x, y)
        y_f = interp1d(x, y)
        y_x = extrap1d(y_f)
        newData.append(y_x(xNew))
        # plt.plot(x, y, 'o', xNew, yNew, '-')
        # plt.show()
    newV = []
    for j in range(0, len(newData[0])):
        v_tmp = []
        for dd in newData:
            v_tmp.append(dd[j])
        newV.append(v_tmp)
    feature_vectors['mxy'].append(newV)
feature_vectors['mxy'] = np.array(feature_vectors['mxy'])

for idx in range(0, len(data_cxt)):
    d = np.array(data_cxt[idx])
    newData = []
    for i in range(1, 7):
        y = d[:, i]
        x = np.arange(0, len(y), 1)
        if len(y) == 1:
            print 'Find a 1-entry-y at #%d iteration!' % idx
            print y
            findOne = True
            break
        xNew = np.linspace(0, len(x), maxCount)
        # yNew = np.interp(xNew, x, y)
        y_f = interp1d(x, y)
        y_x = extrap1d(y_f)
        newData.append(y_x(xNew))
        # plt.plot(x, y, 'o', xNew, yNew, '-')
        # plt.show()
    if findOne:
        findOne = False
        continue
    newV = []
    for j in range(0, len(newData[0])):
        v_tmp = []
        for dd in newData:
            v_tmp.append(dd[j])
        newV.append(v_tmp)
    feature_vectors['cxt'].append(newV)
feature_vectors['cxt'] = np.array(feature_vectors['cxt'])

for idx in range(0, len(data_xr)):
    d = np.array(data_xr[idx])
    newData = []
    for i in range(1, 7):
        y = d[:, i]
        x = np.arange(0, len(y), 1)
        xNew = np.linspace(0, len(x), maxCount)
        # yNew = np.interp(xNew, x, y)
        y_f = interp1d(x, y)
        y_x = extrap1d(y_f)
        newData.append(y_x(xNew))
        # plt.plot(x, y, 'o', xNew, yNew, '-')
        # plt.show()
    newV = []
    for j in range(0, len(newData[0])):
        v_tmp = []
        for dd in newData:
            v_tmp.append(dd[j])
        newV.append(v_tmp)
    feature_vectors['xr'].append(newV)
feature_vectors['xr'] = np.array(feature_vectors['xr'])

print len(feature_vectors['mxy'])
print len(feature_vectors['xr'])
print len(feature_vectors['cxt'])


