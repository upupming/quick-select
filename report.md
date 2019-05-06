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

## 一、实验要求

实现三种中位数选择算法：

- 算法1：排序后选择
- 算法2：确定型中位数线性时间选择算法，《算法设计与分析》第 3 章
- 算法3：中位数选择随机算法

实验内容为：

1. 实现 3 种算法
2. 数据集寻找或生成
3. 运行时间比较，比较准确度（如何衡量）？
4. 扩展性比较
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

