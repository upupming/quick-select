import selector
import numpy as np
import logging

class LazySelector(selector.Selector):
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
            L_p = 0
            H_p = 0
            P = []
            for i in range(length):
                if A[i] <  L:
                    L_p += 1
                if A[i] < H:
                    H_p += 1
                if A[i] >= L and A[i] <= H:
                    P.append(A[i])
            logging.debug(f'(L_p, H_p) = ({L_p}, {H_p})')
            logging.debug(f'P = {P}')

            if L_p <= k and k <= H_p and len(P) <= 4 * selection_len + 1:
                P = np.sort(P)
                logging.debug(f'排序后 P = {P}，返回 P[{k-L_p}]')
                return P[k-L_p]
