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

*列表排序*
```python
%%timeit
a = [12,3,21,3,21,3,21,3,21,4,32,4,23,4,12,3,21,3,123,21,3,21,3,21,321]
sorted(a)
# 914 ns ± 316 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

%%timeit
a = [12,3,21,3,21,3,21,3,21,4,32,4,23,4,12,3,21,3,123,21,3,21,3,21,321]
a.sort()
# 617 ns ± 0.81 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
```

*函数运行(局部变量和全局变量的实现方式)*
```python
%%timeit
a = [12,3,21,3,21,3,21,3,21,4,32,4,23,4,12,3,21,3,123,21,3,21,3,21,321]
sum(a)
# 688 ns ± 244 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

%%timeit
def run():
    a = [12,3,21,3,21,3,21,3,21,4,32,4,23,4,12,3,21,3,123,21,3,21,3,21,321]
    return sum(a)
run()
# 625 ns ± 145 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
```

*导入模块方法(在循环中起效)*
```python
%%timeit
import math
for i in range(1000):
    math.sqrt(i)
# 178 µs ± 47.5 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%%timeit
from math import sqrt
for i in range(1000):
    sqrt(i)
# 132 µs ± 44.6 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
```

*生成器*
```python
%%timeit
[i for i in range(100000)]
# 3.06 ms ± 44.3 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

%%timeit
(i for i in range(100000))
# 510 ns ± 15.7 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
```

*判断顺序*
```python
%%timeit
a = range(3000)
(i for i in a if i % 2 == 0 and i > 2900)
# 755 ns ± 286 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

%%timeit
a = range(3000)
(i for i in a if i > 2900 and i % 2 == 0)
# 577 ns ± 171 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
```

*级联比较*
```python
%%timeit
x, y, z = 1,2,3
x < y and y < z
# 75.6 ns ± 26.1 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)

%%timeit
x, y, z = 1,2,3
x < y  < z
# 67.8 ns ± 12 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
```

> github地址：[https://github.com/skenoy/smartanalysis](https://github.com/skenoy/smartanalysis)
> 本文地址：instance/speed

---

![](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9pLEwFgUObcImwB175s3Nm5eXowgRhE68Nq10K66oBpHiblP6L9XicpeKs9vqUp6NqrYoypNqP37rTA/0?wx_fmt=png)
