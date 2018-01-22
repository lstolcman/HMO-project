#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import os
import route as r


my_dpi = 250
img_size = 2000



if not os.path.exists('images'):
    os.makedirs('images')
for fn in os.listdir("instances"):
    if fn.endswith(".txt"):
        plt.cla()   # Clear axis
        plt.clf()   # Clear figure  
        print('file', fn)
        stops, students = r.process_file('instances/'+fn)
        plt.title(fn)
        plt.scatter(stops[0][0], stops[0][1], marker='o', color='r')
        for p in stops[1:]:
            plt.scatter(p[0], p[1], marker='.', color='b')
        for p in students:
            plt.scatter(p[0], p[1], marker='.', color='k')

        plt.savefig('images/'+fn.split('.')[0]+'.jpg', dpi=my_dpi)
