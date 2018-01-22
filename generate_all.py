#!/usr/bin/env python3

import router as r
import time
import matplotlib.pyplot as plt
import numpy as np
import os
import sys


'''
fn - file name
maxiter - maximum iteration number
maxtries - maximum number of local search if no better result is found, then algorithm is stopped
'''
def process(fn, maxiter, maxtries):
    print('Router init for', fn, end=' ')
    t0 = time.clock()
    router = r.Router(fn)
    stops = router.get_stops()
    students = router.get_students()
    maxwalk = router.get_maxwalk()
    capacity = router.get_capacity()
    print('{0:.5f}s'.format(time.clock()-t0))

    minvalue=float('+Inf')
    tries=0
    min_path_list=None
    min_students_dict=None
    it=0
    while True:
        it+=1
        sys.stdout.write(str(it)+'\r')
        sys.stdout.flush()
        tries+=1
        #print('Local search', it, end=' ')
        t0 = time.clock()
        global_path_list, global_students_dict = None, None
        while global_path_list == None or global_students_dict == None:
            global_path_list, global_students_dict = router.route_local_search()
        #print('{0:.5f}s'.format(time.clock()-t0))
        dist = router.get_distance()
        if dist < minvalue:
            print(dist)
            minvalue = dist
            min_path_list=global_path_list
            min_students_dict=global_students_dict
            tries=0
        if tries>maxtries:
            print('tries {0}, it: {1}'.format(maxtries, it))
            break

        if it>maxiter:
            break

    global_path_list=min_path_list
    global_students_dict=min_students_dict

    with open('results/'+fn.split('/')[1], mode='wt', encoding='utf-8') as f:
        for path in global_path_list:
            f.write(' '.join(str(elem) for elem in path)+'\n')
        f.write('\n')
        for k, v in global_students_dict.items():
            f.write('{0} {1}\n'.format(k, v))
    return [global_path_list, global_students_dict]

if __name__ == '__main__':

    if not os.path.exists('results'):
        os.makedirs('results')
    for fn in os.listdir("instances"):
        if fn.endswith(".txt"):
            print()
            print('next file:', fn)
            process('instances/'+fn, 100, 8)


