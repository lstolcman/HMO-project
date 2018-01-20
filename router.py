#!/usr/bin/env python3

import numpy as np



class Router():
    def __init__(self, routes_fn):
        self.stops = None
        self.students = None
        self.maxwalk = None
        self.capacity = None
        self.student_near_stops = None
        self.stop_near_stops = None

        self.process_file(routes_fn)
        self.generate_student_near_stops()
        self.generate_stop_near_stops()


    def process_file(self, fn):
        self.stops = dict()
        self.students = dict()
        self.maxwalk = None
        self.capacity = None
        stops_max = None
        students_max = None
        current_stop = 0
        current_student = 1
        with open(fn, 'r') as f:
            for num,line in enumerate(f):
                if num == 0:
                    conf = line.split()
                    stops_max = int(conf[0])
                    students_max = int(conf[2])
                    self.maxwalk = float(conf[4])
                    self.capacity = int(conf[7])
                else:
                    if len(line) < 2:
                        ## empty line
                        continue
                    else:
                        s_num, s_x, s_y = [float(v) for v in line.split()]
                        if (current_stop < stops_max):
                            current_stop = current_stop+1
                            self.stops[int(s_num)] = np.array([s_x, s_y])
                        elif (current_student <= students_max):
                            current_student = current_student+1
                            self.students[int(s_num)] = np.array([s_x, s_y])

    def generate_student_near_stops(self):
        '''Calculate distance between students and stops.
        Assign available stops to student
        '''
        self.student_near_stops = dict()
        for k, v in self.students.items():
            available_stops = set()
            for kk, vv in list(self.stops.items())[1:]:
                if np.linalg.norm(v-vv) < self.maxwalk:
                    available_stops.add(kk)
            self.student_near_stops[k] = available_stops

    def generate_stop_near_stops(self):
        '''Calculate distance between stop and other stops'''
        self.stop_near_stops = dict()
        for k, v in list(self.stops.items())[1:]:
            stops_distances = []
            for kk, vv in list(self.stops.items())[1:]:
                if v is not vv:
                    stops_distances.extend([[kk, np.linalg.norm(v-vv)]])
            self.stop_near_stops[k] = sorted(stops_distances, key=lambda x:x[1])

    def get_stops(self):
        return self.stops

    def get_students(self):
        return self.students

    def get_maxwalk(self):
        return self.maxwalk

    def get_capacity(self):
        return self.capacity

    def get_student_near_stops(self):
        return self.student_near_stops

    def get_stop_near_stops(self):
        return self.stop_near_stops



if __name__ == '__main__':
    print('route.py')
