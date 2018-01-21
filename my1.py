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

    '''
    #plot students and stops assigned to them - old way, not using algorithm
    for k, v in student_near_stops.items():
        stud_x, stud_y = students[k]
        for i in v:
            stop_x, stop_y = stops[i]
            plt.plot([stud_x, stop_x], [stud_y, stop_y], 'k-', lw=0.5)

    '''



    '''
    #calculate distance
    for k, v in list(stops.items())[1:]:
        for kk, vv in students.items():
            if np.linalg.norm(v-vv) < maxwalk:
                plt.plot([v[0], vv[0]],[v[1], vv[1]],'k-', lw=0.5)

    #plt.plot([x1, x2],[y1, y2],'k-', lw=0.5)
    '''




    '''
    min_stop_coords = stops[0]
    min_stop_dist = float('+Inf')
    for k, v in list(stops.items())[1:]:
        temp = np.linalg.norm(v-stops[0])
        if temp < min_stop_dist:
            min_stop_dist = temp
            min_stop_coords = v
    #plt.plot([min_stop_coords[0], stops[0][0]],[min_stop_coords[1], stops[0][1]],'r-', lw=0.5)



    last_stop = stops[0]
    while True:
        print()
        print()
        print('stops_not_visited({0})  {1}'.format(len(stops_not_visited), stops_not_visited))
        if len(stops_not_visited) == 1:
            print(last_stop)
            plt.plot([last_stop[0], stops[0][0]], [last_stop[1], stops[0][1]],'r-', lw=0.5)
            break
        z = random.choice(list(stops_not_visited.items())[1:])
        stop_near_student_single = dict()
        stop_near_student_many = dict()
        for student, stops_near in student_near_stops.items():
            if z[0] in stops_near:
                if len(stops_near) == 1:
                    stop_near_student_single[student] = stops_near
                else:
                    stop_near_student_many[student] = stops_near
        print('z', z)
        print('stop_near_student_single({0}  {1}'.format(len(stop_near_student_single), stop_near_student_single))
        print('stop_near_student_many({0})  {1}'.format(len(stop_near_student_many), stop_near_student_many))
        print('last_stop', last_stop)
        #if capacity < len(stop_near_student_single):
        #    pick next nearby stop
        if capacity < len(stop_near_student_single)+len(stop_near_student_many):
            print('capacity too small')
            print('last_stop[0]', last_stop[0])
            plt.plot([last_stop[0], stops[0][0]], [last_stop[1], stops[0][1]],'r-', lw=0.5)
            break
        else:
            plt.plot([last_stop[0], z[1][0]], [last_stop[1], z[1][1]],'r-', lw=0.5)
            del stops_not_visited[z[0]]
            capacity = capacity - len( stop_near_student_many) - len ( stop_near_student_single)
            last_stop = z[1]


    '''


    ## find route algorithm
    global_stops = list(stops.copy().keys())[1:]# [1:] - remove base stop 0 which is unnecessary
    base_stop = global_stops[0]
    global_path_list = []

    #init students list and zero dictionary
    global_students_dict = dict()
    global_students = set(students.copy().keys())
    for s in range(1, len(students)+1):
        global_students_dict[s] = None

    while len(global_students) != 0: ## empty, also some stops can be unassigned. but students must be picked up so thats why this condition
        print('1111111 while len(global_stops) != 0: ## empty')
        local_stops = global_stops.copy()
        next_stop = random.choice(local_stops)
        current_stop = 0 # base stop, always 0, by definition of file format
        print('current_stop', current_stop)
        print('next_stop', next_stop)
        print('local stops', local_stops)
        capacity = router.get_capacity() 
        local_path_list = list()
        while True:
            print(' 2222222222 if next_stop == None:')
            print('local_path_list')
            print(local_path_list)
            print('global_students')
            print(global_students)
            print('next_stop')
            print(next_stop)
            if next_stop == None or len(global_students)==0:
                print('break')
                break

            # get our stop and generate list of students connected with only our stop or many stops
            student_single = set()
            student_many = set()
            print('for student in stop_near_students[next_stop]:')
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
                print('if capacity < ')
                print('local_stops')
                print(local_stops)
                print('next_stop')
                print(next_stop)
                local_stops.remove(next_stop)
                print('cap<len')
                for s in stop_near_stops[next_stop]:
                    if s[0] in local_stops:
                        next_stop = s[0]
            else:
                print('else if capacity <:')
                current_stop = next_stop
                print('current_stop')
                print(current_stop)

                print()
                print('for s in student_single:')
                print(global_students_dict)
                for s in student_single:
                    # wez pojedynczych i przypisz do przystanku
                    global_students_dict[s] = current_stop
                    # usun pojedynczych z listy dostepnych
                    global_students.remove(s)
                print(global_students_dict)

                print()
                print('for s in student_many:')
                print(global_students_dict)
                if capacity > 0:
                    for s in student_many:
                        # wez wielokrotnych i przypisz do przystanku
                        global_students_dict[s] = current_stop
                        # usun pojedynczych z listy dostepnych
                        global_students.remove(s)
                print(global_students_dict)


                print()
                print('local_stops')
                print(local_stops)
                local_stops.remove(current_stop)
                print('local_stops')
                print(local_stops)

                print()
                print('global_stops')
                print(global_stops)
                global_stops.remove(current_stop)
                print('global_stops')
                print(global_stops)

                print()
                print('local_path_list')
                print(local_path_list)
                local_path_list.extend([current_stop])
                print('local_path_list')
                print(local_path_list)

                if capacity > 0 and local_stops == []:
                    print('if capacity > 0 and local_stops == []:')
                    for s in stop_near_stops[next_stop]:
                        if s[0] in local_stops:
                            next_stop = s[0]
                    if np.linalg.norm(current_stop-next_stop) > np.linalg.norm(next_stop-base_stop):
                        next_stop = None
                        global_path_list.extend([local_path_list])
                else:
                    print('else capacity > 0 and local_stops == []:')
                    next_stop = None
                    global_path_list.extend([local_path_list])


    '''
    ## algorytm wyznaczajacy przystankiiii
    #algorytm:

    globalne_przystanki = stops.copy()
    globalna_lista_sciezek = {}
    while globalne_przystanki != empty:
        lokalne_przystanki = globalne_przystanki.copy()
        nastepny_przystanek = random.choice(lokalne_przystanki)
        ostatni_przystanek = baza
        capacity = getcapacity()
        lokalna_lista_sciezek = {}
        while True:
            //if lokalne_przystanki == empty
            if nastepny_przystanek == None
                #plot(ostatni_przystanek, baza)
                break

            if capacity < studenci tylko z tym stopem:
                usun ten przystanek z listy lokalnej stopów
                nastepny_przystanek = najblizszy przystanek od biezacego (lista posortowana od najblizszych do najdalszych)
            else
                #plot(ostatni_przystanek, nastepny_przystanek)
                ostatni_przystanek = nastepny_przystanek
                wez pojedynczych
                usun z kazdego pojedynczego ten stop
                if cap > 0
                    wez z wielu jesli są
                        dla kazdego wzietego ktory mial wiele polaczen
                            usun polaczenie tego przystanku z innymi przystankami
                usun przyst z listy lokalnej stopow
                usun przyst z listy globalnej stopow
                lokalna_lista_sciezek += ??? //dodaj ten stop do lokalnejlisty sciezek ktore powstaly
                if cap>0  && lokalne_przystanki not empty
                    //nastepny_przystanek = najblizszy przystanek od biezacego (lista posortowana od najblizszych do najdalszych), lista zawiera tylko przystanki ktore sa w bazie lokalnych)!! wiec trzeba chyba przeszukiwac
                    nastepny_przystanek = for p in ost_przystanek_nearest: if p in lokalne_przystanki: nastepny przystanek=p, break
                    if dist(ostatni, nastepny) > dist(nastepny,baza)
                        nastepny = None
                        globalna_lista_sciezek += lokalna sciezka
                else
                    nastepny_przystanek = None
                    globalna_lista_sciezek += lokalna sciezka


    '''

    print()
    print()
    print()
    print('global_students_dict')
    print(global_students_dict)

    for k, v in global_students_dict.items():

        stud_x, stud_y = students[k]
        stop_x, stop_y = stops[v]
        plt.plot([stud_x, stop_x],[stud_y, stop_y],'k-', lw=0.5)
        print(k,v)
    print(students)
    print(stops)

    plt.tight_layout()
    #plt.savefig(str(random.randint(1,100))+'.jpg')
    plt.show()



