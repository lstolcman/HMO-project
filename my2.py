#!/usr/bin/env python3

import router
import time


if __name__ == '__main__':
    fn = 'instances/my2.txt'

    print('Router init', end=' ')
    t0 = time.clock()
    router = router.Router(fn)
    stops = router.get_stops()
    students = router.get_students()
    maxwalk = router.get_maxwalk()
    capacity = router.get_capacity()
    print('{0:.5f}s'.format(time.clock()-t0))
    print()



    print('loop')
    for x in range(100):
        print(x, 'Local search', end=' ')
        t0 = time.clock()
        global_path_list, global_students_dict = router.route_local_search()
        print('{0:.5f}s'.format(time.clock()-t0))


