#!/usr/bin/env python3

import numpy as np
import random


class Router():
    def __init__(self, routes_fn):
        self.stops = None
        self.students = None
        self.maxwalk = None
        self.capacity = None
        self.student_near_stops = None
        self.stop_near_stops = None
        self.global_path_list = None
        self.global_students_dict = None

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



    def route_local_search(self):

        ## find route algorithm
        global_stops = list(self.stops.copy().keys())[1:]# [1:] - remove base stop 0 which is unnecessary
        base_stop = global_stops[0]
        global_path_list = []

        #init students list and zero dictionary
        global_students_dict = dict()
        global_students = set(self.students.copy().keys())
        for s in range(1, len(self.students)+1):
            global_students_dict[s] = None

        #stops_debug = [61,37,36] # only first stops, in reverse order
        while len(global_students) != 0: ## empty, also some stops can be unassigned. but students must be picked up so thats why this condition
            local_stops = global_stops.copy()
            next_stop = random.choice(local_stops) # if there's fault with routing, replace this with debug stops list
            #next_stop = stops_debug.pop()
            current_stop = 0 # base stop, always 0, by definition of file format
            capacity = self.capacity
            local_path_list = list()
            while True:
                if next_stop == None or len(global_students)==0:
                    break
                #if len(global_students)>capacity and local_stops == []:
                #    return [None,None] # not feasible solution - conflict: not enough capacity to assign students to stop

                # get our stop and generate list of students connected with only our stop or many stops
                student_single = set()
                student_many = set()
                for student in self.stop_near_students[next_stop]:
                    temp = [x for x in self.student_near_stops[student] if x in global_stops]
                    if student in global_students:
                        if len(temp) == 1:
                            student_single.add(student)
                        elif len(temp) > 1:
                            student_many.add(student)
                        else:
                            raise Exception('Student has no stops!')

                if capacity < len(student_single):#studenci z tym samym stopem
                    if local_stops == []:
                        if len(global_students)>capacity and local_stops == []:
                            return [None,None] # not feasible solution - conflict: not enough capacity to assign students to stop
                        global_path_list.extend([local_path_list])
                        next_stop = None
                        break
                    local_stops.remove(next_stop)
                    for s in self.stop_near_stops[next_stop]:
                        if s[0] in local_stops:
                            next_stop = s[0]
                            break
                else:
                    current_stop = next_stop
                    for s in student_single:
                        # wez pojedynczych i przypisz do przystanku
                        global_students_dict[s] = current_stop
                        # usun pojedynczych z listy dostepnych
                        global_students.remove(s)
                        capacity -= 1

                    for s in student_many:
                        if capacity > 0:
                            # wez wielokrotnych i przypisz do przystanku
                            global_students_dict[s] = current_stop
                            # usun pojedynczych z listy dostepnych
                            global_students.remove(s)
                            capacity -= 1

                    local_stops.remove(current_stop)
                    global_stops.remove(current_stop)
                    local_path_list.extend([current_stop])

                    if capacity > 0 and local_stops != []:
                        for s in self.stop_near_stops[next_stop]:
                            if s[0] in local_stops:
                                next_stop = s[0]
                                break
                        if np.linalg.norm(current_stop-next_stop) > np.linalg.norm(next_stop-base_stop):
                            next_stop = None
                            global_path_list.extend([local_path_list])
                    else:
                        next_stop = None
                        global_path_list.extend([local_path_list])

        self.global_path_list = global_path_list
        self.global_students_dict = global_students_dict
        return [self.global_path_list, self.global_students_dict]


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

    def get_distance(self):
        dist = 0.0
        for path in self.global_path_list:
            for i in range(len(path)+1):
                if i == 0:
                    dist += np.linalg.norm(np.array(self.stops[0])-np.array(self.stops[path[0]]))
                elif i == len(path):
                    dist += np.linalg.norm(np.array(self.stops[0])-np.array(self.stops[path[i-1]]))
                elif i < len(path):
                    dist += np.linalg.norm(np.array(self.stops[path[i]])-np.array(self.stops[path[i-1]]))
        for k, v in self.global_students_dict.items():
            dist += np.linalg.norm(np.array(self.stops[v])-np.array(self.students[k]))
        return dist




if __name__ == '__main__':
    print('route.py')
