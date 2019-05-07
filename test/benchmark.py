import unittest
import sys, os, time
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import selector, linear_selector, lazy_selector
import logging
import numpy as np

class TestPerformance(unittest.TestCase):
    def round_trip(self, A, k, algorithm='naive', log_level=logging.WARNING, distribution='uniform'):
        fileh = logging.FileHandler(f'./log/{algorithm}-benchmark-{distribution}-{logging.getLevelName(log_level)}.log', 'w', encoding='utf-8')
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(message)s')
        fileh.setFormatter(formatter)

        log = logging.getLogger()  # root logger
        for hdlr in log.handlers[:]:  # remove all old handlers
            log.removeHandler(hdlr)
        log.addHandler(fileh)      # set the new handler
        log.setLevel(log_level)

        selector_tester = ''
        if algorithm == 'naive':
            logging.debug('using naive select algorithm')
            selector_tester = selector.Selector()
        if algorithm == 'linear':
            logging.debug('using linear select algorithm')
            selector_tester = linear_selector.LinearSelector()
        elif algorithm == 'lazy':
            logging.debug('using lazy select algorithm')
            selector_tester = lazy_selector.LazySelector()

        begin = time.time()
        x = selector_tester.min(A, k)
        end = time.time()
        logging.warning(f'len(A) = {len(A)}, min(A, {k}) = {x}')
        logging.warning(f'Time used: {end-begin}seconds')
        
        fileh.close()


    def test_uniform(self):
        # logging.warning('Testing uniform distribution')
        A = np.random.uniform(size=1000000)
        self.round_trip(A, 10, 'naive', logging.WARNING, 'uniform')
        # self.round_trip(A, 10, 'linear', logging.WARNING, 'uniform')
        self.round_trip(A, 10, 'lazy', logging.WARNING, 'uniform')
    def test_normalize(self):
        # logging.warning('Testing normalize distribution')
        A = np.random.normal(size=1000000)
        self.round_trip(A, 10, 'naive', logging.WARNING, 'normalize')
        # self.round_trip(A, 10, 'linear', logging.WARNING, 'normalize')
        self.round_trip(A, 10, 'lazy', logging.WARNING, 'normalize')
    def test_zeta(self):
        # logging.warning('Testing zeta distribution')
        A = np.random.zipf(1.01, size=1000000)
        self.round_trip(A, 10, 'naive', logging.WARNING, 'zeta')
        # self.round_trip(A, 10, 'linear', logging.WARNING, 'zeta')
        self.round_trip(A, 10, 'lazy', logging.WARNING, 'zeta')

if __name__ == "__main__":
    unittest.main()