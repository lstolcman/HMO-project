#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import route as rt


if __name__ == '__main__':
    fn = 'instances/my1.txt'
    stops, students, maxwalk, capacity = rt.process_file(fn)
    print(stops)
    print(students)

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
    for k, v in students.items():
        plt.scatter(v[0], v[1], marker='.', s=150, color='xkcd:sky blue', edgecolor='xkcd:dark grey')

    #calculate distance
    for k, v in list(stops.items())[1:]:
        for kk, vv in students.items():
            if np.linalg.norm(v-vv) < maxwalk:
                plt.plot([v[0], vv[0]],[v[1], vv[1]],'k-', lw=0.5)

    #plt.plot([x1, x2],[y1, y2],'k-', lw=0.5)

    min_stop_coords = stops[0]
    min_stop_dist = float('+Inf')
    for k, v in list(stops.items())[1:]:
        temp = np.linalg.norm(v-stops[0])
        if temp < min_stop_dist:
            min_stop_dist = temp
            min_stop_coords = v
    plt.plot([min_stop_coords[0], stops[0][0]],[min_stop_coords[1], stops[0][1]],'r-', lw=0.5)


    plt.tight_layout()
    plt.show()



