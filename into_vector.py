import socket
import scipy.interpolate as si
names = ['mxy', 'xr', 'cxt']
# Convert them into decimals
for name in names:
    with open('data_' + name + '.txt', 'r') as f:
        data = f.readlines()
    newdata = []
    for s in data:
        s = s.replace(' ', '')
        d = []
        i = 0
        while i < 32:
            d.append(socket.htons(int(s[i:i+4], 16)))
            # d.append(s[i:i+4])
            i += 4
        newdata.append(d)
    print newdata.__len__()
    with open('vector_' + name + '.txt', 'w') as f:
        for d in newdata:
            for t in d:
                f.write(str(t) + ' ')
            f.write('\n')
