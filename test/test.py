import unittest
import sys, os, time
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import selector, linear_selector, lazy_selector
import logging
import numpy as np

class TestCorrectness(unittest.TestCase):
    def round_trip(self, algorithm='naive', log_level=logging.WARNING):
        fileh = logging.FileHandler(f'./log/{algorithm}-{logging.getLevelName(log_level)}.log', 'w', encoding='utf-8')
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

        A = np.array([4, 7, 2, 10, 3, 3])
        # x = selector.min(A, 2)
        # logging.warning(f'min({A}, 2) = {x}')
        for i in range(len(A)):
            begin = time.time()
            x = selector_tester.min(A, i)
            end = time.time()
            logging.warning(f'min({A}, {i}) = {x}')
            logging.warning(f'Time used: {end-begin}seconds')
        
        fileh.close()


    def test_naive(self):
        self.round_trip('naive', logging.DEBUG)
        self.round_trip('naive', logging.WARNING)
    def test_linear(self):
        self.round_trip('linear', logging.DEBUG)
        self.round_trip('linear', logging.WARNING)
    def test_lazy(self):
        self.round_trip('lazy', logging.DEBUG)
        self.round_trip('lazy', logging.WARNING)

if __name__ == "__main__":
    unittest.main()