import logging
import cProfile, pstats, io
import linear_selector
import lazy_selector
import numpy as np

# See https://osf.io/upav8/
# Line by line https://github.com/rkern/line_profiler
def profile(fnc):
    
    """A decorator that uses cProfile to profile a function"""
    
    def inner(*args, **kwargs):
        
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner

@profile
def round_trip(algorithm):
    """
    运行一遍算法

    algorithm 算法类型

    c 是指定的阈值
    """
    fileh = logging.FileHandler(f'./log/{algorithm}.log', 'w', encoding='utf-8')
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(message)s')
    fileh.setFormatter(formatter)

    log = logging.getLogger()  # root logger
    for hdlr in log.handlers[:]:  # remove all old handlers
        log.removeHandler(hdlr)
    log.addHandler(fileh)      # set the new handler
    log.setLevel(logging.DEBUG)
    log.setLevel(logging.WARNING)

    selector = ''
    if algorithm == 'linear':
        logging.debug('using linear select algorithm')
        selector = linear_selector.LinearSelector()
    elif algorithm == 'lazy':
        logging.debug('using lazy select algorithm')
        selector = lazy_selector.LazySelector()

    A = np.array([4, 7, 2, 10, 3, 3])
    # x = selector.min(A, 2)
    # logging.warning(f'min({A}, 2) = {x}')
    for i in range(len(A)):
        x = selector.min(A, i)
        logging.warning(f'min({A}, {i}) = {x}')