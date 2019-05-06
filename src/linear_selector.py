import selector
import numpy as np
import logging
from round_trip import *

class LinearSelector(selector.Selector):
    def partition(self, A, x):
        """
        使用 x 对 A 进行划分得到 B，返回划分后 x 的下标 i 满足 B[i] = x, B[i+1] > x 
        A 将会在函数中直接被更改
        """
        pivot = x
        i = -1
        for j in range(len(A)):
            if A[j] < pivot:
                i += 1
                A[i], A[j] = A[j], A[i]
                logging.debug(f'Swaping A[{i}] & A[{j}]')
        return i+1

    def min(self, A, k):
        """
        从数组 A 中选择第 k 小的元素, k in [0, len(A))
        使用线性选择算法
        """
        length = len(A)
        logging.debug(f'算法正在寻找数组 A = {A} 中第 {k} 小的元素')
        logging.debug(f'length = {length}')
        # 递归终止条件
        if (length == 1):
            logging.debug(f'直接返回 A[0]')
            return A[0]
        
        # 先复制一份，避免用户传入的数组被改动
        A = np.copy(A)

        num_of_groups = int(np.ceil(length/5))
        logging.debug(f'分为 {num_of_groups} 组')

        # 如果 length = 11, 应该分为 3 组：0, 1, 2
        for j in range(num_of_groups-1):
            # 排序 0-4(j=0), 5-9(j=1)
            A[j*5:j*5+4] = np.sort(A[j*5:j*5+4])
            logging.debug(f'A[{j*5}:{j*5+4}] sorted: {A[j*5:j*5+4]}')
            # A[...+2] 是求得的中位数
            # 最终求得的中位数放在了 A[0], A[1], A[2] 中
            A[j], A[j*5+2] = A[j*5+2], A[j]
        # , 10-14(j=2)
        # 最后一遍循环可能少于 5 个数，需要特殊处理
        j = num_of_groups - 1
        num_rest = length - j * 5
        B = np.sort(A[j*5:length])
        logging.debug(f'A[{j*5}:{length}] sorted: B = {B}')
        A[j], A[j*5 + num_rest//2] = A[j*5 + num_rest//2], A[j]

        logging.debug(f'中位数前置之后的数组：{A}')

        # Step 3:
        # median of median
        # 总共有 num_of_groups = 3 个数，求其中第 num_of_groups//2 = 1 小的数
        # 如果中位数的个数为偶数，比如 length = 20，那么 num_of_groups//2 = 2，选择第 2 小的数，而不是第 1 小和第 2 小的数的平均值，因为这一步不需要完全精确
        logging.debug(f'mom: 寻找 {A[0:num_of_groups]} 的中位数')
        mom = self.min(A[0:num_of_groups], num_of_groups//2)
        logging.debug(f'mom = {mom}')
        # Step 4:
        # A 将在 partition 方法中被修改，得到划分后的结果
        l = self.partition(A, mom)
        logging.debug(f'l = partition({A}, {mom}) = {l}')

        # Step 5:
        if l == k:
            # A[l] 就是答案
            logging.debug('得到了结果')
            return mom
        elif l > k:
            # 在 A[0] - A[l-1] 中继续找
            logging.debug(f'{l} > {k}，继续寻找 {A[0:l]} 中第 {k} 小的元素')
            return self.min(A[0:l], k)
        else:
            # 在 A[l+1] - A[n-1] 中继续找
            logging.debug(f'{l} < {k}，继续寻找 {A[l+1:length]} 中第 {k-l-1} 小的元素')
            return self.min(A[l+1:length], k - l - 1)


if __name__ == "__main__":
    linearSelector = LinearSelector()
    # # A = np.array([4, 7, 2, 10, 3, 3])
    # A = np.array([7, 3, 2, 10, 3, 4])

    # # 测试 partition 算法的正确性
    # res = linearSelector.partition(A, 7)
    # print(res)
    # print(A)

    # 测试 min 算法的正确性
    # x = linearSelector.min(A, 2)
    # logging.debug(x)
    # round_trip('linear')