## 提速Python

运算速度对于**生物信息**来说非常重要，因为大部分情况下，我们需要自己写代码来提取数据和处理格式，再加上生信领域内的原始数据动辄几千万行，最少也得数万行的基因注释，所以最快地拿到想要的结果才是老板们想要的。

解释型语言（`python`,`perl`等）的平均速度远远不如编译型语言（`C`,`C++`,`Java`等），但解释型语言胜在语法简单明了，代码量少，效率高，很快能处理数据、分析并得到结果，虽然没法比速度，但是自己也不能自暴自弃吧，从数据结构到算法都可以加快程序的运算速度。本文不讨论算法，只通过数据结构等方面提速一下`python`的运算速度。

## 实例
> 以下代码均在`jupyter`中测试速度，不同硬件配置运行速度不一致

*字符串链接(列表变字符串同样的道理)*
```python
%%timeit
tp = (str(i) for i in range(1000))
strs = ''
for i in tp:
    strs += i
# 585 µs ± 225 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%%timeit
tp = (str(i) for i in range(1000))
''.join(tp)
# 223 µs ± 1.07 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
```

*推导式*
```python
%%timeit
a = []
for i in range(1000):
    a.append(i**2)
# 376 µs ± 2.95 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%%timeit
[i**2 for i in range(1000)]
# 344 µs ± 2.51 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
```

*对列表去重*
```python
%%timeit
a = [1,2,2,12,1,1,2,1,2,1,2,12,12,1,22]
d = {}
for i in a:
    d[i] = 0
d.keys()
# 1.04 µs ± 298 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

%%timeit
a = [1,2,2,12,1,1,2,1,2,1,2,12,12,1,22]
set(a)
# 527 ns ± 195 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
```

*for与while*
```python
%%timeit
a = 1000
s = 0
while a > 0:
    s += a
    a -= 1
# 94.2 µs ± 34.8 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%%timeit
s = 0
for i in range(1000):
    s += i
# 46.5 µs ± 194 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
```

*查找元素(包括列表)*
```python
%%timeit
a = range(1000)
d = dict((i,1) for i in a)
500 in d
# 127 µs ± 43.1 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%%timeit
a = range(1000)
s = set(a)
500 in s
# 21 µs ± 79 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
```

*循环索引*
```python
%%timeit
a = range(1000)
for i in range(len(a)):
    a[i]
# 164 µs ± 55.1 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%%timeit
a = range(1000)
for i, v in enumerate(a):
    v
# 41.6 µs ± 470 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
```

以上就是最基本的加速方法，进阶的就属于第三方模块加速：
1. 对于整体python加速，使用numba或pypy（不支持部分模块）
2. 使用由C语言实现的包加速
3. 对pandas类型加速，使用dask
4. 计算正常数据或矩阵数据都可以使用numpy加速
5. IO密集型任务，使用多线程
6. CPU密集型任务，使用多进程，对于生信而言，这个是我们常用的
7. 加速时经常用到的内置包：collections，itertools等等

上面的列表每一个几乎都可以单独写一篇长篇大论了，对数据分析或生信分析来讲，用到的最多也就是数据结构要写好，其次就是numpy，多进程和内置包吧，后面的事情后面再说。

> github地址：[https://github.com/skenoy/smartanalysise](https://github.com/skenoy/smartanalysis)
> 本文地址：instance/speed

![]()

![](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9pLEwFgUObcImwB175s3Nm5eXowgRhE68Nq10K66oBpHiblP6L9XicpeKs9vqUp6NqrYoypNqP37rTA/0?wx_fmt=png)
