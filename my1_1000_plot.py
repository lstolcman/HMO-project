#!/usr/bin/env python3

import router
import time
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    fn = 'instances/my1.txt'

    print('Router init', end=' ')
    t0 = time.clock()
    router = router.Router(fn)
    stops = router.get_stops()
    students = router.get_students()
    maxwalk = router.get_maxwalk()
    capacity = router.get_capacity()
    print('{0:.5f}s'.format(time.clock()-t0))



    minvalue=float('+Inf')
    maxiter=10000
    tries=0
    maxtries=1000
    min_path_list=None
    min_students_dict=None
    it=0
    while True:
        it+=1
        tries+=1
        #print('Local search', it, end=' ')
        t0 = time.clock()
        global_path_list, global_students_dict = None, None
        while global_path_list == None or global_students_dict == None:
            global_path_list, global_students_dict = router.route_local_search()
        #print('{0:.5f}s'.format(time.clock()-t0))
        d = router.get_distance()
        if d < minvalue:
            print(d)
            minvalue = d
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

    with open('my1.txt', mode='wt', encoding='utf-8') as f:
        for path in global_path_list:
            f.write(' '.join(str(elem) for elem in path)+'\n')
        f.write('\n')
        for k, v in global_students_dict.items():
            f.write('{0} {1}\n'.format(k, v))




    #clear all
    plt.cla()
    plt.clf()
    plt.title('{0}\nstops: {1}, students: {2}, maxwalk: {3}, capacity: {4}'.format(fn, len(stops), len(students), maxwalk, capacity))
    #black axis lines
    plt.axhline(0, color='k', lw=0.5)
    plt.axvline(0, color='k', lw=0.5)
    plt.grid(True)
    plt.xticks(np.arange(-13, 14, 1))
    plt.yticks(np.arange(-7, 14, 1))
    plt.axis([-13, 14, -7, 14])
    #plt.minorticks_on()


    #plot students and stops
    plt.scatter(stops[0][0], stops[0][1], marker='o', s=150, color='xkcd:orange', edgecolor='xkcd:dark grey')
    for k, v in list(stops.items())[1:]:
        plt.scatter(v[0], v[1], marker='.', s=150, color='xkcd:pink', edgecolor='xkcd:dark grey')
        plt.text(v[0]+0.1, v[1]+0.1, str(k), fontdict=dict(color='xkcd:purple'))
    for k, v in students.items():
        plt.scatter(v[0], v[1], marker='.', s=150, color='xkcd:sky blue', edgecolor='xkcd:dark grey')
        plt.text(v[0]+0.1, v[1]+0.1, str(k), fontdict=dict(color='xkcd:blue'))

    for path in global_path_list:
        for i in range(len(path)+1):
            if i == 0:
                stop_x, stop_y = stops[path[0]]
                plt.plot([stops[0][0], stop_x],[stops[0][1], stop_y],'r-', lw=0.5)
            elif i == len(path):
                stop_x, stop_y = stops[path[i-1]]
                plt.plot([stops[0][0], stop_x],[stops[0][1], stop_y],'r-', lw=0.5)
            elif i < len(path):
                first_x, first_y = stops[path[i]]
                second_x, second_y = stops[path[i-1]]
                plt.plot([first_x, second_x],[first_y, second_y],'r-', lw=1.5)


    for k, v in global_students_dict.items():
        stud_x, stud_y = students[k]
        stop_x, stop_y = stops[v]
        plt.plot([stud_x, stop_x],[stud_y, stop_y],'k-', lw=0.1)


    plt.tight_layout()
    #plt.savefig(str(random.randint(1,100))+'.jpg')
    plt.show()

