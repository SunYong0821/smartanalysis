## 如何使用多进程加速你的程序（2）

上篇我们说了`Python`进程池的使用方法，对于生物信息来讲使用起来简单有效，但是进程之间是没有顺序或者说通讯的，当写入同一个文件时就会发生错乱，尤其是写入行字符串非常多的时候，最容易出现该问题。

当然解决方案就是加`锁`了，对于文件或者其他方面进行加锁的过程，很容易变成死锁，导致进程堵死，程序卡死状态。。。所以普通的锁模式很不好用，那么最好的解决办法就是重入锁了，如果有兴趣的话，大家搜一下死锁的原理就好了，这里就不再详述了。

那么我们来实现一下重入锁吧！

```python
from multiprocessing import Pool, RLock
from time import sleep
from datetime import datetime

rl = RLock()

def test(i):
    print(i)
    rl.acquire()
    with open('test.txt', 'a') as out:
        out.write(f'{i} is doing...\n')
    rl.release()
    sleep(3)

if __name__ == '__main__':
    p = Pool(4, initargs=(rl,))
    print(datetime.now())
    for i in range(4):
        p.apply_async(test, (i,))
    p.close()
    p.join()
    print(datetime.now())
```

那么我们来看一下这里面的坑吧！

首先就是重入锁不能在函数之后定义，否则就是无效果，最好是全局变量！

其次加锁的位置最好是循环次数比较少，开销比较少的位置，否则会加慢运行速度！

最后`if __name__ == '__main__':`这个也是坑，在某些编辑器运行过程不加会一直报错！所以大家还是按照标准格式做吧。

加了锁之后目前我们就可以在多核的处理器上尽情地玩耍了~~~其实还不是最终的方案，进程之间其实我们还可以共享变量，数据可以放在一起处理，不过这个的坑更多，有些方法根本不能用，网上的教程都是基于2版本的，3版本的又更新的巨快，方法改变了很多，所以坑就很多了，这个找个时间再来测试吧！

那么我们最终的方案是什么呢？当然是分布式+多进程啦~作者做的最好的就是全外显子分布式callsnp方法，速度跟sention的软件比起来时间几乎一致，当然使用的资源不一样。。。

> github：[https://github.com/skenoy/smartanalysis](https://github.com/skenoy/smartanalysis)
> 
> 本文地址：[https://github.com/skenoy/smartanalysis/instance/mutiprocessing/2](https://github.com/skenoy/smartanalysis/instance/mutiprocessing/2)

