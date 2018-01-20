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
                        current_stop = current_stop+1
                        stops[int(s_num)] = np.array([s_x, s_y])
                    elif (current_student <= students_max):
                        current_student = current_student+1
                        students[int(s_num)] = np.array([s_x, s_y])

    return (stops, students, maxwalk, capacity)

if __name__ == '__main__':
    print('route.py')
