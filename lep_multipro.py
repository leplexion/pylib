import multiprocessing

def lep_multipro_runall(*profns):
    multiprocessing.freeze_support()
    pros = []
    for profn in profns:
        pros.append(multiprocessing.Process(target=profn))

    for pro in pros:
        pro.start()

    for pro in pros:
        pro.join()

def lep_multipro_runall_queue(*profns):
    multiprocessing.freeze_support()
    q = multiprocessing.Queue()
    pros = []
    for profn in profns:
        pros.append(multiprocessing.Process(target=profn, args=(q, )))

    for pro in pros:
        pro.start()

    for pro in pros:
        pro.join()