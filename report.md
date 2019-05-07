# 随机算法实验 2 - 比较三种中位数选取算法的效率

<style>
/* Code word wrap for printing PDF */
pre div {
    white-space: pre-wrap;
    word-break: break-all;
}

section.eqno > span {
    width: 5em;
    text-align: right;
}

html,body {
  font-family: 'SimSun' 'Times New Roman';
}
</style>

- [随机算法实验 2 - 比较三种中位数选取算法的效率](#%E9%9A%8F%E6%9C%BA%E7%AE%97%E6%B3%95%E5%AE%9E%E9%AA%8C-2---%E6%AF%94%E8%BE%83%E4%B8%89%E7%A7%8D%E4%B8%AD%E4%BD%8D%E6%95%B0%E9%80%89%E5%8F%96%E7%AE%97%E6%B3%95%E7%9A%84%E6%95%88%E7%8E%87)
  - [一、实验要求](#%E4%B8%80%E5%AE%9E%E9%AA%8C%E8%A6%81%E6%B1%82)
  - [二、实验原理](#%E4%BA%8C%E5%AE%9E%E9%AA%8C%E5%8E%9F%E7%90%86)
    - [算法设计](#%E7%AE%97%E6%B3%95%E8%AE%BE%E8%AE%A1)
      - [SORT-SELECT](#sort-select)
      - [LINEAR-SELECT](#linear-select)
      - [LAZY-SELECT](#lazy-select)
    - [性能测试](#%E6%80%A7%E8%83%BD%E6%B5%8B%E8%AF%95)
      - [Zipf 分布](#zipf-%E5%88%86%E5%B8%83)
  - [三、实验结果](#%E4%B8%89%E5%AE%9E%E9%AA%8C%E7%BB%93%E6%9E%9C)
    - [正确性测试](#%E6%AD%A3%E7%A1%AE%E6%80%A7%E6%B5%8B%E8%AF%95)
      - [SORT-SELECT](#sort-select-1)
      - [LINEAR-SELECT](#linear-select-1)
      - [LAZY-SELECT](#lazy-select-1)
    - [性能测试](#%E6%80%A7%E8%83%BD%E6%B5%8B%E8%AF%95-1)
    - [算法优化](#%E7%AE%97%E6%B3%95%E4%BC%98%E5%8C%96)
      - [LINEAR-SELECT 优化](#linear-select-%E4%BC%98%E5%8C%96)
    - [性能测试（优化之后）](#%E6%80%A7%E8%83%BD%E6%B5%8B%E8%AF%95%E4%BC%98%E5%8C%96%E4%B9%8B%E5%90%8E)
  - [四、对实验结果的理解和分析](#%E5%9B%9B%E5%AF%B9%E5%AE%9E%E9%AA%8C%E7%BB%93%E6%9E%9C%E7%9A%84%E7%90%86%E8%A7%A3%E5%92%8C%E5%88%86%E6%9E%90)
  - [五、实验过程中最值得说起的几个方面](#%E4%BA%94%E5%AE%9E%E9%AA%8C%E8%BF%87%E7%A8%8B%E4%B8%AD%E6%9C%80%E5%80%BC%E5%BE%97%E8%AF%B4%E8%B5%B7%E7%9A%84%E5%87%A0%E4%B8%AA%E6%96%B9%E9%9D%A2)

## 一、实验要求

实现三种中位数选择算法：

- 算法1：排序后选择
- 算法2：确定型中位数线性时间选择算法，《算法设计与分析》第 3 章
- 算法3：中位数选择随机算法

实验内容为：

1. 实现 3 种算法
2. 数据集寻找或生成
3. 运行时间比较，比较准确度（都是正确性算法，验证结果一致性即可）
4. 随机产生服从均匀分布、正态分布、Zipf 分布的数据和均匀选取的 k，开展实验，比较三种算法的性能和扩展性
5. 以恰当、准确、规范地表述实验结果

## 二、实验原理

### 算法设计

问题描述：现有 $n$ 个数，需要设计算法找出这组数中的中位数。

其实本次实验研究的 3 种算法都是可以实现在 $n$ 个不同的数中选取第 $k$ 小的元素（$min
(n, k)$），因此中位数只是一种特殊情况，假设实现的选择算法为 `SELECT`，则如果希望得到中位数，算法调用方式为：

```c
SELECT-MEDIAN
输入：数组 A[0..n-1]
输出：中位数
if n 为偶数
    return ( SELECT(A, n/2-1)+SELECT(A, n/2) )/2
else if n 为奇数
    return SELECT(A, (n-1)/2)
```

算法的总复杂度就取决于 `SELECT` 算法的复杂度，`SELECT` 算法有 3 种实现：

1. `SORT-SELECT`
2. `LINEAR-SELECT`
3. `LAZY-SELECT`

#### SORT-SELECT

算法伪代码描述：

> 注意：算法中的 k 都是以 0 开始的。

```c
SORT-SELECT
输入：数组 A[0..n-1]，需要选取的下标 k
输出：数组中第 k 小的元素
算法：
QuickSort(A)
return A[k]
```

时间复杂度：

$$
T_{SORT-SELECT}(n) = O(n\log n) + O(1) = O(n \log n)
$$

#### LINEAR-SELECT

算法的伪代码描述：

```c
LINEAR-SELECT
输入：数组 A[0..n-1]，需要选取的下标 k
输出：数组中第 k 小的元素
算法：
Step 1: 分组，每组 5 个数，最后一组可能少于 5 个数
    for j = 1 to n/5
Step 2: 将每组的数分别用 InsertionSort 排序，选出每组元素的中位数
        InsertionSort(A[(j-1)*5+1:(j-1)*5+5])
        swap(A[j], A[(j-1)*5+3])
Step 3: 递归调用算法求得这些中位数的中位数 MoM
    x = LINEAR-SELECT(A[1:n/5], n/10)
Step 4: 用 Mom 完成划分
    l = partition(A[1:n], x)
Step 5: 递归，设 x 是中位数的中位数（MoM），划分后完成后其下标为 l。如果 k = l，则返回 x；如果 k < l，则在第一部分递归选取第 k 大的数；如果 k > l，则在第三部分递归选取第 (k-l) 大的数
    if l == k then return x
    else if l > k then return LINEAR-SELECT(A[1:l-1], k)
    else return LINEAR-SELECT(A[l+1:n], k-l)
```

时间复杂度经过[论文](http://i.stanford.edu/pub/cstr/reports/cs/tr/73/349/CS-TR-73-349.pdf)证明，需要的比较操作的次数介于 $1.5n$ 和 $5.43n$ 之间。

时间复杂度的分析这里不再详细介绍，参见《算法设计与分析》第三章，下面直接给出结论：

$$
T_{LINEAR-SELECT}(n) = O(n)
$$

#### LAZY-SELECT

算法的伪代码描述：

```c
LAZY-SELECT
输入：数组 A[0..n-1]，需要选取的下标 k
输出：数组中第 k 小的元素
算法：
1. B = 独立、均匀、可放回地从 A 中随机抽取的 n^(3/4) 个元素
2. 在 O(n) 时间内排序（注：可以证明 m log m 与 n 同阶，如果 m = n^a, a < 1 的话）
3. x = (k/n)n^(3/4) /* (k/n)n^(3/4) = in^(-1/4), 在 n 个元素里面排第 k，那么在 n^(3/4) 个元素里面大约排第 x */
4. l = max{floor(x-sqrt(n)), 0}, h = min{floor(x+sqrt(n), n^{3/4})} /* 在第 x 周围多取 sqrt(n) 的数 */
5. L = min(B, l); H = min(B, h)
6. L_p = Rank(A, L), H_p = Rank(A, H)
7. P = {y in A | L <= y <= H}
8. if min(A, k) in P && |P| <= 4n^{3/4}+1 /* min(A, k) in P 可由 L_p <= k <= H_p 确定 */
9.     then 排序 P，min(A, k) = min(P, (k-L_p))，算法结束
10. else goto 1
```

证明：若 $m = n^a, a \in (0, 1)$，则 $m \log m = O(n)$

$$
\frac{n^a \log n^a}{n} = \frac{a n^a \log n}{n} = an^{-(1-a)}\log n \xlongequal{n \to \infty} 0
$$

该算法属于 Las Vegas 算法，如果得出解，一定是正确的，时间复杂度分析：

算法执行第 1 - 9 步一遍就可以求出 $\min(S, k)$ 的概率为 $p = 1-O(n^{-\frac{1}{4}})$（分析过程参见课件，或者《随机算法》第 3 章），也就是说算法需要 $O(n)$（更具体地说，是 $2n+o(n)$） 次比较就可以求出 $\min(S, k)$ 的概率是 $1-O(n^{-\frac{1}{4}})$。

### 性能测试

随机产生服从均匀分布、正态分布、Zipf 分布的数据和均匀选取的 k，开展实验，比较三种算法的性能和扩展性。

由于三种算法都是一定会给出正确的结论，`LAZY-SELECT` 可能不会得到解，但是按照理论上讲，只要运行次数足够多，就一定会得到解。我们只需要比较三种算法运行的时间快慢即可。

固定生成的数在 $[0, 1)$ 区间，使用不同的分布生成所需要的数，需要了解的是 Zipf 分布。

#### Zipf 分布

根据 [wolfram](http://mathworld.wolfram.com/ZipfDistribution.html)，Zipf 分布又称 Zeta 分布，概率密度函数为：

$$
P(x)=\frac{x^{-s}}{\zeta(s)}
$$

其中 $\zeta$ 是黎曼 $\zeta$ 函数。

Zipf 分布的物理意义与 Zipf 定律有关：给定大量使用的单词样本，任何单词的频率与其在频率表中的排名成反比。因此，字数 $n$ 的频率与 $1/n$ 成比例。

## 三、实验结果

### 正确性测试

执行 `python test/test.py` 即可进行正确性测试，所有结果将被输出到 `log` 文件夹中。

#### SORT-SELECT

计算结果：

```log
min([ 4  7  2 10  3  3], 0) = 2
Time used: 0.0seconds
min([ 4  7  2 10  3  3], 1) = 3
Time used: 0.0seconds
min([ 4  7  2 10  3  3], 2) = 3
Time used: 0.0seconds
min([ 4  7  2 10  3  3], 3) = 4
Time used: 0.0seconds
min([ 4  7  2 10  3  3], 4) = 7
Time used: 0.0seconds
min([ 4  7  2 10  3  3], 5) = 10
Time used: 0.0seconds
```

#### LINEAR-SELECT

计算结果与 `SORT-SELECT` 相同，计算过程（使用 `logging.DEBUG` 等级输出日志）如下：

```log
using linear select algorithm
算法正在寻找数组 A = [ 4  7  2 10  3  3] 中第 0 小的元素
length = 6
分为 2 组
A[0:4] sorted: [ 2  4  7 10]
A[5:6] sorted: B = [3]
中位数前置之后的数组：[ 7  3  2 10  3  4]
mom: 寻找 [7 3] 的中位数
算法正在寻找数组 A = [7 3] 中第 1 小的元素
length = 2
分为 1 组
A[0:2] sorted: B = [3 7]
中位数前置之后的数组：[3 7]
mom: 寻找 [3] 的中位数
算法正在寻找数组 A = [3] 中第 0 小的元素
length = 1
直接返回 A[0]
mom = 3
l = partition([3 7], 3) = 0
0 < 1，继续寻找 [7] 中第 0 小的元素
算法正在寻找数组 A = [7] 中第 0 小的元素
length = 1
直接返回 A[0]
mom = 7
l = partition([ 3  2  3  4  7 10], 7) = 4
4 > 0，继续寻找 [3 2 3 4] 中第 0 小的元素
算法正在寻找数组 A = [3 2 3 4] 中第 0 小的元素
length = 4
分为 1 组
A[0:4] sorted: B = [2 3 3 4]
中位数前置之后的数组：[3 2 3 4]
mom: 寻找 [3] 的中位数
算法正在寻找数组 A = [3] 中第 0 小的元素
length = 1
直接返回 A[0]
mom = 3
l = partition([2 3 3 4], 3) = 1
1 > 0，继续寻找 [2] 中第 0 小的元素
算法正在寻找数组 A = [2] 中第 0 小的元素
length = 1
直接返回 A[0]
min([ 4  7  2 10  3  3], 0) = 2
Time used: 0.006973743438720703seconds
算法正在寻找数组 A = [ 4  7  2 10  3  3] 中第 1 小的元素
length = 6
分为 2 组
A[0:4] sorted: [ 2  4  7 10]
A[5:6] sorted: B = [3]
中位数前置之后的数组：[ 7  3  2 10  3  4]
mom: 寻找 [7 3] 的中位数
算法正在寻找数组 A = [7 3] 中第 1 小的元素
length = 2
分为 1 组
A[0:2] sorted: B = [3 7]
中位数前置之后的数组：[3 7]
mom: 寻找 [3] 的中位数
算法正在寻找数组 A = [3] 中第 0 小的元素
length = 1
直接返回 A[0]
mom = 3
l = partition([3 7], 3) = 0
0 < 1，继续寻找 [7] 中第 0 小的元素
算法正在寻找数组 A = [7] 中第 0 小的元素
length = 1
直接返回 A[0]
mom = 7
l = partition([ 3  2  3  4  7 10], 7) = 4
4 > 1，继续寻找 [3 2 3 4] 中第 1 小的元素
算法正在寻找数组 A = [3 2 3 4] 中第 1 小的元素
length = 4
分为 1 组
A[0:4] sorted: B = [2 3 3 4]
中位数前置之后的数组：[3 2 3 4]
mom: 寻找 [3] 的中位数
算法正在寻找数组 A = [3] 中第 0 小的元素
length = 1
直接返回 A[0]
mom = 3
l = partition([2 3 3 4], 3) = 1
得到了结果
min([ 4  7  2 10  3  3], 1) = 3
Time used: 0.0029969215393066406seconds
算法正在寻找数组 A = [ 4  7  2 10  3  3] 中第 2 小的元素
length = 6
分为 2 组
A[0:4] sorted: [ 2  4  7 10]
A[5:6] sorted: B = [3]
中位数前置之后的数组：[ 7  3  2 10  3  4]
mom: 寻找 [7 3] 的中位数
算法正在寻找数组 A = [7 3] 中第 1 小的元素
length = 2
分为 1 组
A[0:2] sorted: B = [3 7]
中位数前置之后的数组：[3 7]
mom: 寻找 [3] 的中位数
算法正在寻找数组 A = [3] 中第 0 小的元素
length = 1
直接返回 A[0]
mom = 3
l = partition([3 7], 3) = 0
0 < 1，继续寻找 [7] 中第 0 小的元素
算法正在寻找数组 A = [7] 中第 0 小的元素
length = 1
直接返回 A[0]
mom = 7
l = partition([ 3  2  3  4  7 10], 7) = 4
4 > 2，继续寻找 [3 2 3 4] 中第 2 小的元素
算法正在寻找数组 A = [3 2 3 4] 中第 2 小的元素
length = 4
分为 1 组
A[0:4] sorted: B = [2 3 3 4]
中位数前置之后的数组：[3 2 3 4]
mom: 寻找 [3] 的中位数
算法正在寻找数组 A = [3] 中第 0 小的元素
length = 1
直接返回 A[0]
mom = 3
l = partition([2 3 3 4], 3) = 1
1 < 2，继续寻找 [3 4] 中第 0 小的元素
算法正在寻找数组 A = [3 4] 中第 0 小的元素
length = 2
分为 1 组
A[0:2] sorted: B = [3 4]
中位数前置之后的数组：[4 3]
mom: 寻找 [4] 的中位数
算法正在寻找数组 A = [4] 中第 0 小的元素
length = 1
直接返回 A[0]
mom = 4
l = partition([3 4], 4) = 1
1 > 0，继续寻找 [3] 中第 0 小的元素
算法正在寻找数组 A = [3] 中第 0 小的元素
length = 1
直接返回 A[0]
min([ 4  7  2 10  3  3], 2) = 3
Time used: 0.005997180938720703seconds
算法正在寻找数组 A = [ 4  7  2 10  3  3] 中第 3 小的元素
length = 6
分为 2 组
A[0:4] sorted: [ 2  4  7 10]
A[5:6] sorted: B = [3]
中位数前置之后的数组：[ 7  3  2 10  3  4]
mom: 寻找 [7 3] 的中位数
算法正在寻找数组 A = [7 3] 中第 1 小的元素
length = 2
分为 1 组
A[0:2] sorted: B = [3 7]
中位数前置之后的数组：[3 7]
mom: 寻找 [3] 的中位数
算法正在寻找数组 A = [3] 中第 0 小的元素
length = 1
直接返回 A[0]
mom = 3
l = partition([3 7], 3) = 0
0 < 1，继续寻找 [7] 中第 0 小的元素
算法正在寻找数组 A = [7] 中第 0 小的元素
length = 1
直接返回 A[0]
mom = 7
l = partition([ 3  2  3  4  7 10], 7) = 4
4 > 3，继续寻找 [3 2 3 4] 中第 3 小的元素
算法正在寻找数组 A = [3 2 3 4] 中第 3 小的元素
length = 4
分为 1 组
A[0:4] sorted: B = [2 3 3 4]
中位数前置之后的数组：[3 2 3 4]
mom: 寻找 [3] 的中位数
算法正在寻找数组 A = [3] 中第 0 小的元素
length = 1
直接返回 A[0]
mom = 3
l = partition([2 3 3 4], 3) = 1
1 < 3，继续寻找 [3 4] 中第 1 小的元素
算法正在寻找数组 A = [3 4] 中第 1 小的元素
length = 2
分为 1 组
A[0:2] sorted: B = [3 4]
中位数前置之后的数组：[4 3]
mom: 寻找 [4] 的中位数
算法正在寻找数组 A = [4] 中第 0 小的元素
length = 1
直接返回 A[0]
mom = 4
l = partition([3 4], 4) = 1
得到了结果
min([ 4  7  2 10  3  3], 3) = 4
Time used: 0.004000663757324219seconds
算法正在寻找数组 A = [ 4  7  2 10  3  3] 中第 4 小的元素
length = 6
分为 2 组
A[0:4] sorted: [ 2  4  7 10]
A[5:6] sorted: B = [3]
中位数前置之后的数组：[ 7  3  2 10  3  4]
mom: 寻找 [7 3] 的中位数
算法正在寻找数组 A = [7 3] 中第 1 小的元素
length = 2
分为 1 组
A[0:2] sorted: B = [3 7]
中位数前置之后的数组：[3 7]
mom: 寻找 [3] 的中位数
算法正在寻找数组 A = [3] 中第 0 小的元素
length = 1
直接返回 A[0]
mom = 3
l = partition([3 7], 3) = 0
0 < 1，继续寻找 [7] 中第 0 小的元素
算法正在寻找数组 A = [7] 中第 0 小的元素
length = 1
直接返回 A[0]
mom = 7
l = partition([ 3  2  3  4  7 10], 7) = 4
得到了结果
min([ 4  7  2 10  3  3], 4) = 7
Time used: 0.0019989013671875seconds
算法正在寻找数组 A = [ 4  7  2 10  3  3] 中第 5 小的元素
length = 6
分为 2 组
A[0:4] sorted: [ 2  4  7 10]
A[5:6] sorted: B = [3]
中位数前置之后的数组：[ 7  3  2 10  3  4]
mom: 寻找 [7 3] 的中位数
算法正在寻找数组 A = [7 3] 中第 1 小的元素
length = 2
分为 1 组
A[0:2] sorted: B = [3 7]
中位数前置之后的数组：[3 7]
mom: 寻找 [3] 的中位数
算法正在寻找数组 A = [3] 中第 0 小的元素
length = 1
直接返回 A[0]
mom = 3
l = partition([3 7], 3) = 0
0 < 1，继续寻找 [7] 中第 0 小的元素
算法正在寻找数组 A = [7] 中第 0 小的元素
length = 1
直接返回 A[0]
mom = 7
l = partition([ 3  2  3  4  7 10], 7) = 4
4 < 5，继续寻找 [10] 中第 0 小的元素
算法正在寻找数组 A = [10] 中第 0 小的元素
length = 1
直接返回 A[0]
min([ 4  7  2 10  3  3], 5) = 10
Time used: 0.0019979476928710938seconds
```

#### LAZY-SELECT

结果仍然与 `SORT-SELECT`，计算过程如下：

```log
using lazy select algorithm
要在 [ 4  7  2 10  3  3] 中选择第 0 小的元素
选出的 B 经排序后为 [ 4  7 10]
x = 0
(l, h) = (0, 2)
(L, H) = (4, 10)
(L_p, H_p) = (3, 5)
P = [ 4  7 10]
选出的 B 经排序后为 [3 4 4]
x = 0
(l, h) = (0, 2)
(L, H) = (3, 4)
(L_p, H_p) = (1, 3)
P = [4 3 3]
选出的 B 经排序后为 [ 4 10 10]
x = 0
(l, h) = (0, 2)
(L, H) = (4, 10)
(L_p, H_p) = (3, 5)
P = [ 4  7 10]
选出的 B 经排序后为 [4 4 7]
x = 0
(l, h) = (0, 2)
(L, H) = (4, 7)
(L_p, H_p) = (3, 4)
P = [4 7]
选出的 B 经排序后为 [ 3  3 10]
x = 0
(l, h) = (0, 2)
(L, H) = (3, 10)
(L_p, H_p) = (1, 5)
P = [ 4  7 10  3  3]
选出的 B 经排序后为 [3 4 7]
x = 0
(l, h) = (0, 2)
(L, H) = (3, 7)
(L_p, H_p) = (1, 4)
P = [4 7 3 3]
选出的 B 经排序后为 [3 3 4]
x = 0
(l, h) = (0, 2)
(L, H) = (3, 4)
(L_p, H_p) = (1, 3)
P = [4 3 3]
选出的 B 经排序后为 [2 3 3]
x = 0
(l, h) = (0, 2)
(L, H) = (2, 3)
(L_p, H_p) = (0, 1)
P = [2 3 3]
排序后 P = [2 3 3]
min([ 4  7  2 10  3  3], 0) = 2
Time used: 0.0060002803802490234seconds
要在 [ 4  7  2 10  3  3] 中选择第 1 小的元素
选出的 B 经排序后为 [2 4 4]
x = 0
(l, h) = (0, 2)
(L, H) = (2, 4)
(L_p, H_p) = (0, 3)
P = [4 2 3 3]
排序后 P = [2 3 3 4]
min([ 4  7  2 10  3  3], 1) = 3
Time used: 0.0seconds
要在 [ 4  7  2 10  3  3] 中选择第 2 小的元素
选出的 B 经排序后为 [2 3 3]
x = 1
(l, h) = (0, 2)
(L, H) = (2, 3)
(L_p, H_p) = (0, 1)
P = [2 3 3]
选出的 B 经排序后为 [3 4 4]
x = 1
(l, h) = (0, 2)
(L, H) = (3, 4)
(L_p, H_p) = (1, 3)
P = [4 3 3]
排序后 P = [3 3 4]
min([ 4  7  2 10  3  3], 2) = 3
Time used: 0.0009992122650146484seconds
要在 [ 4  7  2 10  3  3] 中选择第 3 小的元素
选出的 B 经排序后为 [3 3 4]
x = 1
(l, h) = (0, 2)
(L, H) = (3, 4)
(L_p, H_p) = (1, 3)
P = [4 3 3]
排序后 P = [3 3 4]
min([ 4  7  2 10  3  3], 3) = 4
Time used: 0.00099945068359375seconds
要在 [ 4  7  2 10  3  3] 中选择第 4 小的元素
选出的 B 经排序后为 [2 3 7]
x = 2
(l, h) = (0, 2)
(L, H) = (2, 7)
(L_p, H_p) = (0, 4)
P = [4 7 2 3 3]
排序后 P = [2 3 3 4 7]
min([ 4  7  2 10  3  3], 4) = 7
Time used: 0.00099945068359375seconds
要在 [ 4  7  2 10  3  3] 中选择第 5 小的元素
选出的 B 经排序后为 [ 4  7 10]
x = 3
(l, h) = (0, 2)
(L, H) = (4, 10)
(L_p, H_p) = (3, 5)
P = [ 4  7 10]
排序后 P = [ 4  7 10]
min([ 4  7  2 10  3  3], 5) = 10
Time used: 0.0010001659393310547seconds
```

### 性能测试

执行 `python test/benchmark.py` 即可进行正确性测试。

在实际测试中发现一个有趣的现象，在测试 zipf 分布生成的数据的时候，对于这样的数组（当 $\zeta$ 太大时）：

```log
[1 1 1 1 1 1 1 2 1 1 2]
```

因为元素的值基本上是一样的，`LAZY-SELECT` 最终选出来的 `P` 长度永远都满足不了结束条件，因此算法会永远都结束不了。因此修改了 zipf 分布的参数再次进行实验，得到如下的结果：

|分布类型|算法|A 的长度|结果|所用的时间|
|-------|----|---|----------|-------|
|均匀分布|SORT-SELECT (`numpy`)|1000|min(A, 10) = 0.006654379877537031|0.0030896663665771484seconds|
|均匀分布|LINEAR-SELECT|1000|min(A, 10) = 0.006654379877537031|0.0seconds|
|均匀分布|LAZY-SELECT|1000|min(A, 10) = 0.006654379877537031|0.0030896663665771484seconds|
|正态分布|SORT-SELECT (`numpy`)|1000|min(A, 10) = -2.140409828353999|0.0seconds|
|正态分布|LINEAR-SELECT|1000|min(A, 10) = -2.140409828353999|0.2992517948150635seconds|
|正态分布|LAZY-SELECT|1000|min(A, 10) = -2.140409828353999|0.015314340591430664seconds|
|Zipf 分布，$\zeta=1.01$|SORT-SELECT (`numpy`)|1000|min(A, 10) = 1|0.0seconds|
|Zipf 分布，$\zeta=1.01$|LINEAR-SELECT|1000|min(A, 10) = 1|0.19576048851013184seconds|
|Zipf 分布，$\zeta=1.01$|LAZY-SELECT|1000|min(A, 10) = 1|0.003997802734375seconds|

从表中可以看出 `SORT-SELECT` 几乎不耗费任何时间（因为我直接调用了 numpy 的 sort 函数，numpy 应该优化做的比较好，所以比较快），而 `LINEAR-SORT` 明显比 `LAZY-SORT` 慢得多。

为了显示 `SORT-SELECT` 的不足，特意增大数据量进行测试，只关注数据量和运行时间，得到下面的运行结果：

|分布类型|算法|A 的长度|所用的时间|
|-------|----|---|----------|
|均匀分布|SORT-SELECT (`numpy`)|10,000|0.0019943714141845703seconds|
|均匀分布|LINEAR-SELECT|10,000|8.294952154159546seconds|
|均匀分布|LAZY-SELECT|10,000|0.20388269424438477seconds|
|正态分布|SORT-SELECT (`numpy`)|10,000|0.0seconds|
|正态分布|LINEAR-SELECT|10,000|3.501344680786133seconds|
|正态分布|LAZY-SELECT|10,000|0.03799915313720703seconds|
|Zipf 分布，$\zeta=1.01$|SORT-SELECT (`numpy`)|10,000|0.0009999275207519531seconds|
|Zipf 分布，$\zeta=1.01$|LINEAR-SELECT|10,000|20.213204383850098seconds|
|Zipf 分布，$\zeta=1.01$|LAZY-SELECT|10,000|0.006994009017944336seconds|

从测试来看，最快的还是 `SORT-SELECT`，`LAZY-SORT` 次之，`LINEAR-SORT` 最慢。理论上 `SORT-SELECT` 应该最慢才对。可能是 numpy 优化做的很不错。

### 算法优化

与其他同学的运行时间进行比较之后，发现主要有两个优化点：

1. `LINEAR-SELECT` 算法在《算法导论》 9.2 中有更加高效的实现。
2. 在算法需要得到某个元素的 `rank` 时，如果使用 `partition` 函数，需要的运行时间为 $\Theta(n)$，但是里面有 `swap` 操作。由于 `LAZY-SELECT` 算法中只需要得到 rank，并不需要真正地对元素进行划分，我们可以单独自己写一个循环，同时还可以在这个循环内面生成 P，从而节省了很多时间。
<!-- 3. 后来在实际测试中又发现了一个小的优化空间：`logging.debug` 虽然只有在 `level` 设置为 -->

#### LINEAR-SELECT 优化

由于算法导论中为它取名为『RANDOMIZED-SELECT』，因此我这里也采用了这个名字。

```c
RANDOMIZED-SELECT
输入：数组 A[0..n-1]，需要选取的下标 k
输出：数组中第 k 小的元素
算法：
if n == 1
    return A[0]
q = RANDOMIZED-PARTITION(A)
if q == k:
    return A[q]
elseif k < q:
    return RANDOMIZED-SELECT(A[0:q-1], k)
else return RANDOMIZED-SELECT(A[q+1:], k-q)
```

### 性能测试（优化之后）

> 因为 Zipf 数据本身的特点，处理耗时较长，所以取样数较少。

|分布类型|算法|A 的长度|所用的时间|
|-------|----|---|----------|
|均匀分布|SORT-SELECT (`numpy`)|1,000,000|0.24885845184326172seconds|
|均匀分布|LINEAR-SELECT|1,000,000|3.949763059616089seconds|
|均匀分布|LAZY-SELECT|1,000,000|4.454483985900879seconds|
|正态分布|SORT-SELECT (`numpy`)|1,000,000|0.12593460083007812seconds|
|正态分布|LINEAR-SELECT|1,000,000|0.5047116279602051seconds|
|正态分布|LAZY-SELECT|1,000,000|2.378643274307251seconds|
|Zipf 分布，$\zeta=1.01$|SORT-SELECT (`numpy`)|10,000|0.0010001659393310547seconds|
|Zipf 分布，$\zeta=1.01$|LINEAR-SELECT|10,000|0.9494802951812744seconds|
|Zipf 分布，$\zeta=1.01$|LAZY-SELECT|10,000|0.03298377990722656seconds|

可以看到，在数据量比较小的时候（10,000 左右），`LAZY-SELECT` 比 `LINEAR-SELECT` 快很多，随着数据量的增加，其优势逐渐消失，甚至还会慢一些，这与算法运行次数增加有关。

## 四、对实验结果的理解和分析

1. `numpy` 自己实现的排序算法比较快，与自己实现的算法不具有可比性。
2. `LAZY-SELECT` 算法具有优越性，但是也会有缺点，需要进一步改善，较少运行遍数，同时使之能够处理特殊的数据。

## 五、实验过程中最值得说起的几个方面

1. 老师之前提到过一个想法，对于不同的集合，我们采取不同的交集连接算法，以达到最优的性能。选择算法也是如此，对于不同分布的数据，我们应该选取最适合这种分布的算法进行选择。
2. 性能优化，参见前文。