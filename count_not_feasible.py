#!/usr/bin/env python3

import router
import time


if __name__ == '__main__':
    fn = 'instances/sbr3.txt'

    print('Router init', end=' ')
    t0 = time.clock()
    router = router.Router(fn)
    stops = router.get_stops()
    students = router.get_students()
    maxwalk = router.get_maxwalk()
    capacity = router.get_capacity()
    print('{0:.5f}s'.format(time.clock()-t0))
    print()



    nf=0
    print('loop')
    it=1000
    for i in range(it):
        print('{0}/{1} ({2}%)'.format(i, it, 100*(i/it)))
        t0 = time.clock()
        global_path_list, global_students_dict = router.route_local_search()
        if global_path_list == None and global_students_dict == None:
            nf+=1
    print('not feasible solutions: {0}/{1} ({2}%)'.format(nf,it, 100*(nf/it)))


