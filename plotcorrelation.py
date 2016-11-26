#!/usr/bin/env python3

"""Plot the correlation between different parameters from a csv file
created by ./recheck_all_result_layouts.py --csv --regularity"""

import pylab as pl
# pl.ion()
import csv
with open("/tmp/evo.txt") as f:
    c = csv.reader(f)            
    a = [i for i in c]
b = pl.array([[float(j) for j in i[1:]] for i in a[1:]]).transpose()
print(list(zip(range(len(a)), a[0][1:])))
c = pl.corrcoef(b)
c = pl.ma.array(c, mask=pl.isnan(c))
pl.imshow(c, interpolation="nearest", vmin=min(c.min(), -c.max()), vmax=max(c.max(), -c.min()), cmap=pl.cm.RdYlBu_r)
pl.colorbar()
pl.show()
