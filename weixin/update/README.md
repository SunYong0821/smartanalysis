## python3.0之后更新了什么？

> `python3`跟`python2`差别比较大，且2在2020年就不再更新了，所以还是建议大家使用`python3`。

`python3`现在的版本是3.7，3.8版本的beta已经出来了，但是之间更新了什么内容，却很多人没有关心过，也不知道选择哪些版本，我们来简单聊聊（以上仅针对数据分析和生物信息分析）。

1. 直接从3.6开始吧，个人认为比较重要的是`f-string`，变量内插。`perl`相比较而然非常简单，仅仅`$`加变量名即可，3.6之前的`python`个人认为比较难用，如下：
```python
# 3.6之前
print('{}'.format(var))
# 3.6之后
print(f'{var}')
```
是不是少写很多代码？
2. 3.6还有一个重要的就是字典键不再无序，而是有序的。这个就尴尬了，因为很多语言设定字典（哈希）键是无顺序的，有序的很有可能会影响之前的代码，不过好处就是内存减少20%~30%，这个数字还是很给力的！不过一定要注意这一项，**3.6字典键是有序的**！！！
3. 而3.7比较重要的是检测环境中的语言模式，默认是`utf-8`模式，不同终端这一点很恼火，这一次直接先默认了！
4. 3.8更新还没来，不过有几点很有意思：
   1. 首先是许多内置方法和函数已经**加速20％~50％**，给力！
   2. 多进程处理模块终于有共享内存的方法了，涉及到多进程处理
   3. 赋值表达式新特性
   4. 部分模块加速，不错~

说了这么多，其实就一个意思————请用新版`python`，生命苦短，节省时间和内存！（不像其他语言，要么十几年没更新，要么更新没啥大进展）


> github：[https://github.com/skenoy/smartanalysis](https://github.com/skenoy/smartanalysis)
> 本文地址：[https://github.com/skenoy/smartanalysis/weixin/update](https://github.com/skenoy/smartanalysis/weixin/update)

![]()

![](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9pLEwFgUObcImwB175s3Nm5eXowgRhE68Nq10K66oBpHiblP6L9XicpeKs9vqUp6NqrYoypNqP37rTA/0?wx_fmt=png)
