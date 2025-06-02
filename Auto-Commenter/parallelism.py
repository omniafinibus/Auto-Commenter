from multiprocessing import Pool, Process, cpu_count

PROC_POOL = None
CPU_COUNT = cpu_count()
if CPU_COUNT >= 3:
    PROC_POOL = Pool(processes=3)
elif CPU_COUNT == 2:
    PROC_POOL = Pool(processes=2)
