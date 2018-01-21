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

    #plot students and stops assigned to them
    for k, v in student_near_stops.items():
        stud_x, stud_y = students[k]
        for i in v:
            stop_x, stop_y = stops[i]
            plt.plot([stud_x, stop_x], [stud_y, stop_y], 'k-', lw=0.5)
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
    global_stops = stops.copy()
    base_stop = global_stops[0]
    del global_stops[0] # remove base stop 0 which is unnecessary
    global_path_list = []

    global_students_dict = dict()
    for s in range(1, len(students)+1):
        global_students_dict[s] = None

    while len(global_stops) != 0: ## empty
        local_stops = global_stops.copy()
        next_stop = random.choice(list(local_stops.items()))
        last_stop = base_stop
        print('last_stop', last_stop)
        print('next_stop', next_stop)
        print('local stops', local_stops)
        capacity = router.get_capacity() 
        local_path_list = []
        while True:
            if next_stop == None:
                break
            if capacity < 4:#studenci z tym samym stopem
                del local_stops[next_stop]
                next_stop = None#closest stop from available
            else:
                last_stop = next_stop
                break
                #wez pojedyncze
                #usun z kazdego pojedynczego
                #if capacity > 0:
                #    wez z wielu jesli są
                #        dla kazdego wzietego ktory mial wiele polaczen
                #            usun polaczenie tego przystanku z innymi przystankami
                #usun przyst z listy lokalnej stopow
                #del local_stops[next_stop]
                #usun przyst z listy globalnej stopow
                #del global_stops[next_stop]
                #lokalna_lista_sciezek += ??? //dodaj ten stop do lokalnejlisty sciezek ktore powstaly
                #if cap>0  && len(local_stops) != 0:
                    #nastepny_przystanek = najblizszy przystanek od biezacego (lista posortowana od najblizszych do najdalszych), lista zawiera tylko przystanki ktore sa w bazie lokalnych)!! wiec trzeba chyba przeszukiwac
                #    nastepny_przystanek = for p in ost_przystanek_nearest: if p in lokalne_przystanki: nastepny przystanek=p, break
                #    if dist(ostatni, nastepny) > dist(nastepny,baza)
                #        next_stop = None
                #        global_path_list.extend([[local_path_list]])
                #else
                #    next_stop = None
                #    global_path_list.extend([[local_path_list]])
        break


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

    plt.tight_layout()
    plt.show()



