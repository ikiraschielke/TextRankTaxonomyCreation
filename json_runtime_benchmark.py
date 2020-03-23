# BENCHMARKING FOR JSON FILES

import json
import random
import time
import matplotlib.pyplot as plt


Ns = 10, 100, 1000, 10000, 100000, 200000, 300000, 600000, 1000000
def json_runtime_bechmark(Ns):
    print('called')
    times=[]
    for N in Ns:
        l = [random.random() for i in range(N)]
        t0 = time.time()
        s = json.dumps(l)
        t1 = time.time()
        dt = t1-t0
        times.append(round(dt,5))
    print("Length of JSON dump list:'{},'Time for serialization in seconds:'{}".format(N,times)
    return times

erg=json_runtime_bechmark(Ns)



plt.plot(Ns,erg)
plt.ylabel('Length of JSON dump list')
plt.xlabel(Time for serialization in seconds)
plt.show()

