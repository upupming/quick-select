# min(A, k) algorithm

Author: Li Yiming

- Sort select: O(n log n)
- Linear select: 1.5n ~ 5.43n
- Lazy select: 2n + o(n)

See my [report](report.md) (in Chinese) for more technical information.

Run test cases and see the logs under `log` folder (you have to manually create it if not exist):

```bash
python test/test.py
```

The log file with `WARNING` is a simple version of log, and `DEBUG` is a more verbose version of log.

For example, the `lazy-WARNING.log` file has only the summary of the algorithm result and time used:

```txt
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

But the `lazy-DEBUG.log` file contains all the steps taken during the algorithm, it will be useful for you to understand the algorithm quickly.