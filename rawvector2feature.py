import numpy as np
import matplotlib.pylab as plt
from scipy.interpolate import interp1d
from scipy.spatial.distance import euclidean
from sklearn.decomposition import PCA
from scipy.spatial import ConvexHull
from sklearn.ensemble import RandomForestClassifier
import os.path


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
if not os.path.isfile('interped_raw_mxy.npy'):
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
    # print maxCount
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
                print('Find a 1-entry-y at #%d iteration!' % idx)
                print(y)
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

    print(len(feature_vectors['mxy']))
    print(len(feature_vectors['xr']))
    print(len(feature_vectors['cxt']))

    np.save('interped_raw_mxy', feature_vectors['mxy'])
    np.save('interped_raw_xr', feature_vectors['xr'])
    np.save('interped_raw_cxt', feature_vectors['cxt'])

# compute the feature vectors
mxy = np.load('interped_raw_mxy.npy')
cxt = np.load('interped_raw_cxt.npy')
xr = np.load('interped_raw_xr.npy')
if not os.path.isfile('feas.npy'):
    mxy_avg = []
    cxt_avg = []
    xr_avg = []

    for d in mxy:
        sum = np.zeros((1, 6))
        for dd in d:
            sum += dd
        sum /= len(d)
        mxy_avg.append(sum)

    for d in cxt:
        sum = np.zeros((1, 6))
        for dd in d:
            sum += dd
        sum /= len(d)
        cxt_avg.append(sum)

    for d in xr:
        sum = np.zeros((1, 6))
        for dd in d:
            sum += dd
        sum /= len(d)
        xr_avg.append(sum)

    # print len(mxy_avg), len(xr_avg), len(cxt_avg)
    mxy_fea = []
    cxt_fea = []
    xr_fea = []
    fea = []
    for i in range(0, len(mxy)):
        mxy_fea.append([euclidean(x, avg) for avg in mxy_avg[i] for x in mxy[i]])

    for i in range(0, len(mxy)):
        mxy_fea.append([euclidean(x, avg) for avg in mxy_avg[i] for x in mxy[i]])

    for i in range(0, len(mxy)):
        mxy_fea.append([euclidean(x, avg) for avg in mxy_avg[i] for x in mxy[i]])

    for d in mxy_fea:
        fea.append(d)
    for d in cxt_fea:
        fea.append(d)
    for d in xr_fea:
        fea.append(d)

    print(len(fea))

    fea = np.array(fea)
    np.save('feas', fea)
fea = np.load('feas.npy')
# print(fea)

pca = PCA(n_components=10)

feas = pca.fit_transform(fea)

# print(fea)
feas = np.array(feas)
print(feas)
hull = ConvexHull(feas, qhull_options="Qx, E0.03")

print(len(fea[0]))

rf = RandomForestClassifier()
rf.fit(fea[0:50], [1 for i in range(0, 50)])
t = rf.predict(fea[51:117])
print(t)