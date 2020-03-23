# BENCHMARKING FOR XML files
import time
from bs4 import BeautifulSoup
import os
import matplotlib.pyplot as plt


def bench_ET():
    total_len = 0
    Ns = [10, 100, 200, 400, 600, 800] 
    times = []
    i=0
    t0 = time.time()


    with os.scandir('pil/pil') as files:
        for entry in files:
            with open(entry, "rb", ) as f:
                contents = f.read()

            tree = BeautifulSoup(contents,'lxml')
            result = []
            

            for v in tree.recursiveChildGenerator():
                if v.name == 'block' or v.name == 'div':
                    result.append(v.text)

                    total_len += len(result)

            if i in Ns:
                t1 = time.time()
                it = t1-t0
                times.append(round(it,5))
            

            i +=1


    t2 = time.time()
    dt = t2-t0
    erg = "runtime in sec {}, n found tags {}".format(dt,total_len)

    return erg, times





erg = bench_ET()
print(erg)

#Plot results
Ns = [10, 100, 200, 400, 600, 800] 
erg_lxml= [1.06534, 6.00524, 20.81301, 37.39166, 68.84769, 87.28456]
erg_html = [1.2323768138885498, 7.624139308929443, 16.164966344833374, 33.03722810745239, 49.40533804893494, 75.67143034934998]

plt.plot(Ns,erg_html)
plt.ylabel('N of files processed')
plt.xlabel('Time in seconds')
plt.show()
