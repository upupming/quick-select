import selector
import numpy as np
import logging

class LinearSelector(selector.Selector):
    def partition(self, A):
        length = len(A)
        pivot = A[length-1]
        logging.debug(f'基准元素为 {pivot}')
        i = -1
        for j in range(length-1):
            if A[j] <= pivot:
                i += 1
                logging.debug(f'Swaping A[{i}] & A[{j}]')
                A[i], A[j] = A[j], A[i]
        A[i+1], A[length-1] = A[length-1], A[i+1]
        return i+1

    def random_partition(self, A):
        """
        随机生成 x，使用 x 对 A 进行划分得到 B，返回划分后 x 的下标 i 满足 B[i] = x, B[i+1] > x 
        A 将会在函数中直接被更改
        """
        length = len(A)
        pivot_index = np.random.randint(length)
        A[pivot_index], A[length-1] = A[length-1], A[pivot_index]
        return self.partition(A)
        

    def min(self, A, k):
        """
        从数组 A 中选择第 k 小的元素, k in [0, len(A))
        使用线性选择算法
        """
        length = len(A)
        logging.debug(f'LINEAR-SELECT 算法正在寻找数组 A = {A} 中第 {k} 小的元素')
        logging.debug(f'length = {length}')
        # 递归终止条件
        if (length == 1):
            logging.debug(f'直接返回 A[0]')
            return A[0]
        
        # 先复制一份，避免用户传入的数组被改动
        A = np.copy(A)

        q = self.random_partition(A)
        logging.debug(f'划分后 A = {A}，第 {q} 的元素为 {A[q]}')
        if q == k:
            logging.debug(f'找到了 A[{q}] = {A[q]}')
            return A[q]
        elif k < q:
            logging.debug(f'{k} < {q}，递归调用 min(A[0:{q-1}], {k})')
            return self.min(A[0:q], k)
        else:
            logging.debug(f'{k} > {q}，递归调用 min(A[{q+1}:], {k-q-1})')
            return self.min(A[q+1:], k-q-1)