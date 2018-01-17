#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt


def process_file(fn):
    stops = []
    students = []
    nstops = 0
    nstudents = 0
    with open(fn, 'r') as f:
        for n,l in enumerate(f):
            if (n==0):
                conf = l.split(' ')
                nstops = int(conf[0])
                nstudents = int(conf[2])
            if n >= 2 and (nstops > 0 or nstudents > 0):
                if len(l)>1:
                    lsplit = l.split()
                    if nstops > 0:
                        nstops = nstops -1
                        stops.append([float(lsplit[1]), float(lsplit[2])])
                    elif nstudents >= 0:
                        nstudents = nstudents-1
                        students.append([float(lsplit[1]), float(lsplit[2])])

    return [np.array(stops), np.array(students)]

if __name__ == '__main__':
    fn = 'instances/sbr1.txt'
    stops, students = process_file(fn)
    plt.cla()
    plt.clf()
    plt.title(fn)
    plt.scatter(stops[0][0], stops[0][1], marker='o', color='r')
    for p in stops[1:]:
        plt.scatter(p[0], p[1], marker='.', color='b')
    for p in students:
        plt.scatter(p[0], p[1], marker='.', color='k')

    plt.show()


