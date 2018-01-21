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
        self.generate_stop_near_students()


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
        out = dict( <student_id> : set( <stop_id>, <stop_id>, <stop_id>, ...)
                    <student_id> : set( <stop_id>, <stop_id>, <stop_id>, ...)
                  )
        '''
        self.student_near_stops = dict()
        for k, v in self.students.items():
            available_stops = set()
            for kk, vv in list(self.stops.items())[1:]:
                if np.linalg.norm(v-vv) < self.maxwalk:
                    available_stops.add(kk)
            self.student_near_stops[k] = available_stops
        print()
        print('self.student_near_stops')
        print(self.student_near_stops)
        print()

    def generate_stop_near_stops(self):
        '''Calculate distance between stop and other stops
        out = dict( <stop_id> : tuple( tuple(<stop_id>, <distance>), tuple(<stop_id>, <distance>), ...)
                    <stop_id> : tuple( tuple(<stop_id>, <distance>), tuple(<stop_id>, <distance>), ...)
                  )
        '''
        self.stop_near_stops = dict()
        for k, v in list(self.stops.items())[1:]:
            stops_distances = []
            for kk, vv in list(self.stops.items())[1:]:
                if v is not vv:
                    stops_distances.extend([tuple([kk, np.linalg.norm(v-vv)])])
            self.stop_near_stops[k] = tuple(sorted(stops_distances, key=lambda x:x[1]))
        print()
        print('self.stop_near_stops')
        print(self.stop_near_stops)
        print()

    def generate_stop_near_students(self):
        '''Calculate distance between students and stops.
        Assign available student to stops
        out = dict( <stop_id> : set( <student_id>, <student_id>, <student_id>, ...)
                    <stop_id> : set( <student_id>, <student_id>, <student_id>, ...)
                  )
        '''
        self.stop_near_students = dict()
        for k, v in list(self.stops.items())[1:]:
            if k == 0: continue
            available_students = set()
            for kk, vv in self.students.items():
                if np.linalg.norm(v-vv) < self.maxwalk:
                    available_students.add(kk)
            self.stop_near_students[k] = available_students
        print()
        print('self.stop_near_students')
        print(self.stop_near_students)
        print()

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

    def get_stop_near_students(self):
        return self.stop_near_students



if __name__ == '__main__':
    print('route.py')
