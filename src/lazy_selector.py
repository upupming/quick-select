import selector
import numpy as np
import logging

class LazySelector(selector.Selector):
    def partition(self, A, x):
        """
        使用 x 对 A 进行划分得到 B，返回划分后 x 的下标 i 满足 B[i] = x, B[i+1] > x 
        A 将【不会】在函数中被更改
        """
        pivot = x
        A = np.copy(A)
        i = -1
        for j in range(len(A)):
            if A[j] < pivot:
                i += 1
                A[i], A[j] = A[j], A[i]
                # logging.debug(f'Swaping A[{i}] & A[{j}]')
        return i+1
    def min(self, A, k):
        """
        从数组 A 中选择第 k 小的元素, k in [0, len(A))
        使用 LAZY-SELECT 随机/选择算法
        """
        logging.debug(f'要在 {A} 中选择第 {k} 小的元素')
        length = len(A)
        selection_len = int((length ** (3/4)))
        
        while True:
            B = np.random.choice(A, selection_len)
            B = np.sort(B)
            logging.debug(f'选出的 B 经排序后为 {B}')
            x = int((k/length) * (length ** (3/4)))
            logging.debug(f'x = {x}')
            l = int(max(x-np.sqrt(length), 0))
            h = int(min(x+np.sqrt(length), selection_len-1))
            logging.debug(f'(l, h) = ({l}, {h})')
            L = B[l]
            H = B[h]
            logging.debug(f'(L, H) = ({L}, {H})')
            L_p = self.partition(A, L)
            H_p = self.partition(A, H)
            logging.debug(f'(L_p, H_p) = ({L_p}, {H_p})')
            P = np.extract(np.logical_and(A>=L, A<=H), A)
            logging.debug(f'P = {P}')

            if L_p <= k and k <= H_p and len(P) <= 4 * selection_len + 1:
                P = np.sort(P)
                logging.debug(f'排序后 P = {P}')
                return P[k-L_p]
