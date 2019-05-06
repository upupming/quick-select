import numpy as np

class Selector:
    def __init__(self):
        pass
    def min(self, A, k):
        """
        从数组 A 中选择第 k 小的元素, k in [0, len(A))
        使用排序后选择算法
        """
        return np.sort(A)[k]