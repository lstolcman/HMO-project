#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt


def process_file(fn):
    stops = dict()
    students = dict()
    stops_max = 0
    students_max = 0
    current_stop = 0
    current_student = 1
    maxwalk = 0.0
    capacity = 0
    with open(fn, 'r') as f:
        for num,line in enumerate(f):
            if num == 0:
                conf = line.split()
                stops_max = int(conf[0])
                students_max = int(conf[2])
                maxwalk = float(conf[4])
                capacity = int(conf[7])
            else:
                if len(line) < 2:
                    ## empty line
                    continue
                else:
                    s_num, s_x, s_y = [float(v) for v in line.split()]
                    if (current_stop < stops_max):
                        current_stop = current_stop + 1
                        stops[int(s_num)] = [s_x, s_y]
                    elif (current_student <= students_max):
                        current_student = current_student +1
                        students[int(s_num)] = [s_x, s_y]


    return [stops, students, maxwalk, capacity]

if __name__ == '__main__':
    fn = 'instances/sbr1.txt'
    stops, students, maxwalk, capacity = process_file(fn)
    print(stops)
    for k,v in stops.items():
        print(k,v)
    print(students)
    '''
    #clear all
    plt.cla()
    plt.clf()
    plt.title('{0}\nstops: {1}, students: {2}, maxwalk: {3}, capacity: {4}'.format(fn, len(stops), len(students), maxwalk, capacity))
    #black axis lines
    plt.axhline(0, color='k', lw=0.5)
    plt.axvline(0, color='k', lw=0.5)
    plt.grid(True)
    plt.axis([-13, 14, -7, 14])
    plt.xticks(np.arange(-13, 14, 1))
    plt.yticks(np.arange(-7, 14, 1))
    plt.minorticks_on()

    print(students)
    #plot students and stops
    plt.scatter(stops[0][0], stops[0][1], marker='o', s=150, color='xkcd:orange', edgecolor='xkcd:dark grey')
    for p in stops[1:]:
        plt.scatter(p[0], p[1], marker='.', s=150, color='xkcd:pink', edgecolor='xkcd:dark grey')
    for p in students:
        plt.scatter(p[0], p[1], marker='.', s=150, color='xkcd:sky blue', edgecolor='xkcd:dark grey')

    #calculate distance
    for s in stops[1:]:
        for st in students:
            if np.linalg.norm(s-st) < maxwalk:
                plt.plot([s[0], st[0]],[s[1], st[1]],'k-', lw=0.5)

    #plt.plot([x1, x2],[y1, y2],'k-', lw=0.5)

    min_stop_coords = stops[0]
    min_stop_dist = float('+Inf')
    for s in stops[1:]:
        temp = np.linalg.norm(s-stops[0])
        if temp < min_stop_dist:
            min_stop_dist = temp
            min_stop_coords = s
    plt.plot([min_stop_coords[0], stops[0][0]],[min_stop_coords[1], stops[0][1]],'r-', lw=0.5)


    plt.tight_layout()
    plt.show()
    '''

