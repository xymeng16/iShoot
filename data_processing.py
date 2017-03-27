# Shooting motion recognition -- data precessing
# Author: Xiangyi Meng
# Data: 24 March, 2017
new_xy = []
new_new_xy = []
with open('mxy.txt') as f:
    data = f.readlines()
for s in data:
    i = s.find('0200dc01 144c02bc 591da302 7b064d09')
    if i != -1:
        idx = data.index(s)
print idx
for s in data:
    if data.index(s) >= idx:
        new_xy.append(s)
print new_xy[0]
for s in new_xy:
    i = s.find('notified')
    if i != -1:
        new_new_xy.append(s[i + 11:s.__len__() - 2] + '\n')

with open('data_mxy.txt', 'w') as f:
    f.writelines(new_new_xy)

filenames = ['cxt.txt', 'xr.txt']
for i in range(0, 2):
    with open(filenames[i]) as f:
        data = f.readlines()
    print data.__len__()
    newdata = []
    for s in data:
        j = s.find('notified')
        if j != -1:
            newdata.append(s[j + 11:s.__len__() - 2] + '\n')
    print newdata.__len__()

    with open('data_' + filenames[i], 'w') as f:
        f.writelines(newdata)
