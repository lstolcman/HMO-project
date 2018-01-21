#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import random
import router


if __name__ == '__main__':
    fn = 'instances/my1.txt'

    router = router.Router(fn)

    stops = router.get_stops()
    stops_not_visited = stops.copy()
    students = router.get_students()
    maxwalk = router.get_maxwalk()
    capacity = router.get_capacity()

    student_near_stops = router.get_student_near_stops()
    stop_near_stops = router.get_stop_near_stops()
    stop_near_students = router.get_stop_near_students()

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

    ## find route algorithm
    global_stops = list(stops.copy().keys())[1:]# [1:] - remove base stop 0 which is unnecessary
    base_stop = global_stops[0]
    global_path_list = []

    #init students list and zero dictionary
    global_students_dict = dict()
    global_students = set(students.copy().keys())
    for s in range(1, len(students)+1):
        global_students_dict[s] = None

    #stops_debug = [7, 7, 6, 1, 3] # only first stops, in reverse order
    while len(global_students) != 0: ## empty, also some stops can be unassigned. but students must be picked up so thats why this condition
        local_stops = global_stops.copy()
        next_stop = random.choice(local_stops) # if there's fault with routing, replace this with debug stops list
        #next_stop = stops_debug.pop()
        current_stop = 0 # base stop, always 0, by definition of file format
        capacity = router.get_capacity() 
        local_path_list = list()
        while True:
            if next_stop == None or len(global_students)==0:
                break

            # get our stop and generate list of students connected with only our stop or many stops
            student_single = set()
            student_many = set()
            for student in stop_near_students[next_stop]:
                temp = [x for x in student_near_stops[student] if x in global_stops]
                if student in global_students:
                    if len(temp) == 1:
                        student_single.add(student)
                    elif len(temp) > 1:
                        student_many.add(student)
                    else:
                        raise Exception('Student has no stops!')

            if capacity < len(student_single):#studenci z tym samym stopem
                if local_stops == []:
                    global_path_list.extend([local_path_list])
                    next_stop = None
                    break
                local_stops.remove(next_stop)
                for s in stop_near_stops[next_stop]:
                    if s[0] in local_stops:
                        next_stop = s[0]
            else:
                current_stop = next_stop
                for s in student_single:
                    # wez pojedynczych i przypisz do przystanku
                    global_students_dict[s] = current_stop
                    # usun pojedynczych z listy dostepnych
                    global_students.remove(s)
                    capacity -= 1

                if capacity > 0:
                    for s in student_many:
                        # wez wielokrotnych i przypisz do przystanku
                        global_students_dict[s] = current_stop
                        # usun pojedynczych z listy dostepnych
                        global_students.remove(s)
                        capacity -= 1
                local_stops.remove(current_stop)
                global_stops.remove(current_stop)
                local_path_list.extend([current_stop])

                if capacity > 0 and local_stops != []:
                    for s in stop_near_stops[next_stop]:
                        if s[0] in local_stops:
                            next_stop = s[0]
                            break
                    if np.linalg.norm(current_stop-next_stop) > np.linalg.norm(next_stop-base_stop):
                        next_stop = None
                        global_path_list.extend([local_path_list])
                else:
                    next_stop = None
                    global_path_list.extend([local_path_list])


    with open('result.txt', mode='wt', encoding='utf-8') as f:
        for path in global_path_list:
            f.write(' '.join(str(elem) for elem in path)+'\n')
        f.write('\n')
        for k, v in global_students_dict.items():
            f.write('{0} {1}\n'.format(k, v))

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
        plt.plot([stud_x, stop_x],[stud_y, stop_y],'k-', lw=0.5)


    plt.tight_layout()
    #plt.savefig(str(random.randint(1,100))+'.jpg')
    plt.show()



