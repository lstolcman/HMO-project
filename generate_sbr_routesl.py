#!/usr/bin/env python3

import router as r
import time
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import datetime


'''
fn - file name
maxiter - maximum iteration number
maxtries - maximum number of local search if no better result is found, then algorithm is stopped
tm - how much time to compute result, in minutes
'''
def process(fn, maxiter, maxtries, tm=None):
    print('Router init for', fn)
    print('time constraint: {0}\nmax iterations={1}\nmax tries for better result={2}'.format(tm, maxiter, maxtries))
    t0 = time.clock()
    router = r.Router(fn)
    stops = router.get_stops()
    students = router.get_students()
    maxwalk = router.get_maxwalk()
    capacity = router.get_capacity()
    print('Time: {0:.6f}s'.format(time.clock()-t0))

    minvalue=float('+Inf')
    tries=0
    min_path_list=None
    min_students_dict=None
    it=0
    twhile = time.clock()
    while True:
        if tm != None:
            if (time.clock()-twhile) > tm*60:
                print('time limit reached: {0}  ({1}m)'.format(time.clock()-twhile, tm))
                break
        it+=1
        sys.stdout.write(str(it)+'\r')
        sys.stdout.flush()
        tries+=1
        #print('Local search', it, end=' ')
        #t0 = time.clock()
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
        if maxtries and tries>maxtries:
            print('tries {0}, it: {1}'.format(maxtries, it))
            break

        if maxiter and it>maxiter:
            break

    if tm ==None:
        print('time elapsed: {0:.2f}s'.format(time.clock()-twhile))

    if (tm == None):
        outfname = 'res-un-'+(fn.split('/')[1]).split('.')[0]+'.txt'
    else:
        outfname = 'res-'+str(tm)+'m-'+(fn.split('/')[1]).split('.')[0]+'.txt'


    with open('results/results.txt', mode='a', encoding='utf-8') as f:
        f.write('{6} {4} dist={3} iter={5} time_constraint={0} maxiter={1} maxtries={2}\n'.format(tm, maxiter, maxtries, dist, outfname, it, datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))


    global_path_list=min_path_list
    global_students_dict=min_students_dict


    print(outfname)
    with open('results/'+outfname, mode='wt', encoding='utf-8') as f:
        for path in global_path_list:
            f.write(' '.join(str(elem) for elem in path)+'\n')
        f.write('\n')
        for k, v in global_students_dict.items():
            f.write('{0} {1}\n'.format(k, v))
    return [global_path_list, global_students_dict]

if __name__ == '__main__':

    print('================')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    print('================')
    '''
    try:
        os.remove('results/results.txt')
    except OSError:
        pass
    '''
    with open('results/results.txt', mode='a', encoding='utf-8') as f:
        f.write('\n')
        f.write('\n')
        f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        f.write('\n')

    maxiter = 100
    maxtries = 10
    if not os.path.exists('results'):
        os.makedirs('results')
    for fn in os.listdir("instances"):
        if fn.startswith('sbr') and fn.endswith('.txt'):
            print()
            print()
            print('next file:', fn)
            process('instances/'+fn, maxiter, maxtries)
            print()
            process('instances/'+fn, maxiter=None, maxtries=None, tm=1)
            print()
            process('instances/'+fn, maxiter=None, maxtries=None, tm=5)
            print('----------------')
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
            print('----------------')


