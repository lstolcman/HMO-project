#!/usr/bin/env python3

import router
import time
import matplotlib.pyplot as plt
import numpy as np
import time


def plot_stops(stops):
    plt.scatter(stops[0][0], stops[0][1], marker='o', s=150, color='xkcd:orange', edgecolor='xkcd:dark grey')
    for k, v in list(stops.items())[1:]:
        plt.scatter(v[0], v[1], marker='.', s=150, color='xkcd:pink', edgecolor='xkcd:dark grey')
        plt.text(v[0]+0.1, v[1]+0.1, str(k), fontdict=dict(color='xkcd:purple'))

def plot_students(students):
    for k, v in students.items():
        plt.scatter(v[0], v[1], marker='.', s=150, color='xkcd:sky blue', edgecolor='xkcd:dark grey')
        plt.text(v[0]+0.1, v[1]+0.1, str(k), fontdict=dict(color='xkcd:blue'))

def plot_student_potential_assignments(student_near_stops):
    for k, v in student_near_stops.items():
        stud_x, stud_y = students[k]
        for i in v:
            stop_x, stop_y = stops[i]
            plt.plot([stud_x, stop_x], [stud_y, stop_y], 'k:', lw=1.0)

def route_local_search(iterations):
    t0 = time.clock()
    minvalue = float('+Inf')
    min_path_list = None
    min_students_dict = None
    print('Local search: {0} iterations'.format(iterations))
    for i1 in range(iterations):
        global_path_list, global_students_dict = router.route_local_search()
        if global_path_list == None or global_students_dict == None:
            i1=i1-1
        dist = router.get_distance()
        if dist < minvalue:
            print('dist:', dist)
            minvalue = dist
            min_path_list = global_path_list
            min_students_dict = global_students_dict
    print('{0:.5f}s'.format(time.clock()-t0))
    return [min_path_list, min_students_dict]

def init_pyplot():
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
    plt.tight_layout()


if __name__ == '__main__':
    fn = 'instances/my1.txt'

    print('Router init', end=' ')
    t0 = time.clock()
    router = router.Router(fn)
    stops = router.get_stops()
    students = router.get_students()
    maxwalk = router.get_maxwalk()
    capacity = router.get_capacity()
    student_near_stops = router.get_student_near_stops()
    print('{0:.5f}s'.format(time.clock()-t0))


    print('Router local search', end=' ')
    t0 = time.clock()
    paths, stud_assign = route_local_search(1000)
    print('{0:.5f}s'.format(time.clock()-t0))

    init_pyplot()
    plot_students(students)
    plot_stops(stops)

    plt.savefig('my1-stops.jpg')

    plot_student_potential_assignments(student_near_stops)

    plt.savefig('my1-potential-stops.jpg')

    #init again to clear potential routes
    init_pyplot()
    plot_students(students)
    plot_stops(stops)

    for k, v in stud_assign.items():
        stud_x, stud_y = students[k]
        stop_x, stop_y = stops[v]
        plt.plot([stud_x, stop_x],[stud_y, stop_y],'b-', lw=1.0)

    plt.savefig('my1-stops-assignment.jpg')

    for path in paths:
        for i in range(len(path)+1):
            if i == 0:
                stop_x, stop_y = stops[path[0]]
                plt.plot([stops[0][0], stop_x],[stops[0][1], stop_y],'r-', lw=1.0)
            elif i == len(path):
                stop_x, stop_y = stops[path[i-1]]
                plt.plot([stops[0][0], stop_x],[stops[0][1], stop_y],'r-', lw=1.0)
            elif i < len(path):
                first_x, first_y = stops[path[i]]
                second_x, second_y = stops[path[i-1]]
                plt.plot([first_x, second_x],[first_y, second_y],'r-', lw=1.0)


    plt.savefig('my1-route.jpg')

