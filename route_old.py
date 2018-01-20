#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys


def process_file(fn):
    stops = []
    students = []
    nstops = 0
    nstudents = 0
    maxwalk = 0.0
    capacity = 0
    with open(fn, 'r') as f:
        for n,l in enumerate(f):
            if (n==0):
                conf = l.split()
                nstops = int(conf[0])
                nstudents = int(conf[2])
                maxwalk = float(conf[4])
                capacity = int(conf[7])
            if n >= 2 and (nstops > 0 or nstudents > 0):
                if len(l)>1:
                    lsplit = l.split()
                    if nstops >= 0:
                        nstops = nstops -1
                        stops.append([float(lsplit[1]), float(lsplit[2])])
                    elif nstudents >= 0:
                        nstudents = nstudents-1
                        students.append([float(lsplit[1]), float(lsplit[2])])

    return [np.array(stops), np.array(students), maxwalk, capacity]

if __name__ == '__main__':
    fn = 'instances/sbr3.txt'
    stops, students, maxwalk, capacity = process_file(fn)
    #clear all
    plt.cla()
    plt.clf()
    plt.title('{0}\nstops: {1}, students: {2}, maxwalk: {3}, capacity: {4}'.format(fn, len(stops), len(students), maxwalk, capacity))
    #black axis lines
    plt.axhline(0, color='k', lw=0.5)
    plt.axvline(0, color='k', lw=0.5)
    plt.scatter(stops[0][0], stops[0][1], marker='o', s=150, color='xkcd:orange', edgecolor='xkcd:dark grey')
    for p in stops[1:]:
        plt.scatter(p[0], p[1], marker='.', s=150, color='xkcd:pink', edgecolor='xkcd:dark grey')
    for p in students:
        plt.scatter(p[0], p[1], marker='.', s=150, color='xkcd:sky blue', edgecolor='xkcd:dark grey')

    asn = len(stops)
    astn = len(students)
    for sn,s in enumerate(stops[1:]):
        sys.stdout.write('stops {0}/{1}\r'.format(sn, asn))
        sys.stdout.flush()
        for st in students:
            if np.linalg.norm(s-st) < maxwalk:
                plt.plot([s[0], st[0]],[s[1], st[1]],'k-', lw=0.51)
    #plt.plot([x1, x2],[y1, y2],'k-', lw=0.5)

    min_stop_coords = stops[0]
    min_stop_dist = float('+Inf')
    for s in stops[1:]:
        temp = np.linalg.norm(s-stops[0])
        if temp < min_stop_dist:
            print(min_stop_dist)
            min_stop_dist = temp
            min_stop_coords = s
    plt.plot([min_stop_coords[0], stops[0][0]],[min_stop_coords[1], stops[0][1]],'r-', lw=0.5)


    plt.show()


