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

## Benchmark

You can run benchmark with command, the output will be written to files under `log` folder:

```bash
python test/benchmark.py
```

> Zipf distribution seems more difficult to select, so I only tested the case when the length of A is 10,000.

|Distribution|Algorithm|Length of A|Time used|
|-------|----|---|----------|
|Uniform|SORT-SELECT (`numpy`)|1,000,000|0.24885845184326172seconds|
|Uniform|LINEAR-SELECT|1,000,000|3.949763059616089seconds|
|Uniform|LAZY-SELECT|1,000,000|4.454483985900879seconds|
|Normalize|SORT-SELECT (`numpy`)|1,000,000|0.12593460083007812seconds|
|Normalize|LINEAR-SELECT|1,000,000|0.5047116279602051seconds|
|Normalize|LAZY-SELECT|1,000,000|2.378643274307251seconds|
|Zipf with ζ = 1.01|SORT-SELECT (`numpy`)|10,000|0.0010001659393310547seconds|
|Zipf with ζ = 1.01|LINEAR-SELECT|10,000|0.9494802951812744seconds|
|Zipf with ζ = 1.01|LAZY-SELECT|10,000|0.03298377990722656seconds|