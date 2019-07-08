## 如何使用多进程加速你的程序（1）

前面说了，对于生物信息来讲，大部分时间都在运算和比较，基本没有空闲的时间停下来，由于`Python`的GIL（全局锁）的影响，多线程在生信领域很难应用到的，所以多进程才是我们所需要的加速方法！！！

我们先来看看我之前写的`perl`的多线程吧：
```perl
#!perl
use warnings;
use strict;
use threads;
use Thread::Semaphore;

my $j=0;
my $thread;
my $max_threads=5;
my $semaphore=Thread::Semaphore->new($max_threads);

print localtime(time),"\n";
while()
{    
	last if($j>10);

    $j=$j+1;
    $semaphore->down();
    my $thread=threads->new(\&ss,$j,$j); 
    $thread->detach();
}

&waitquit; 

print localtime(time),"\n";

sub ss() 
{   my ($t,$s)=@_;
    sleep($t);
#    print "$s\t",scalar(threads->list()),"\t$j\t",localtime(time),"\n";
    $semaphore->up();
}

sub waitquit
{    
	print "Waiting to quit...\n";
    my $num=0;
    while($num < $max_threads)
    {    
		$semaphore->down();
        $num++;
        print "$num thread quit...\n";
    }
    print "All $max_threads thread quit\n";
}
```

总的来讲，在`perl`里面我们需要控制信号来判断是否加入新的任务，而且写起来相当负责和混乱。。。

那我们来看看`Python`怎么实现多进程的吧！
```python
from multiprocessing import Pool
from time import sleep
from datetime import datetime

def test(i):
    print(f'{i} is doing...')
    sleep(3)

if __name__ == '__main__':
    p = Pool(4)
    print(datetime.now())
    for i in range(4):
        p.apply_async(test, (i,))
    p.close()
    p.join()
    print(datetime.now())
```

如果按照正常来讲这个`test`函数，需要3*4=12秒才能完成工作，如果我们开启了多进程：

![起效了！](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9pS0UgxQ8xWIhD7JRKFbgtenFBMNPFALPu2ctP8FrX0HzfiblHxeVEcoDxOptViaMrDD6ltkicYLLFrw/0?wx_fmt=png)

仅需要3秒多就完成了！！！(jupyter notebook不能测试，编辑器问题)

那么我们在生信领域可以用在什么地方呢？查询位点的所在位置，处理BAM/Fastq文件，大数据量的过滤程序等等，只要涉及到计算时间长，都可以往里面扔！！！

其实在`Pool`里面还有个新特性需要了解一下：
```python
# 接收方法和参数
# p.apply_async
# 接收迭代器
# p.map_async
# 使用map_async实现上面的，需要改造一下test
p.map_async(test, range(4))
```

根据以上注释所示，如果不需要传递多个参数，可以使用`p.map_async`更方便！大家可以测试一下！

我们的程序现在的速度就快很多了！但是仍然有些问题。。。多进程是很快，但是多进程写到同一个文件怎么办？会不会出问题？答案是会！那么下次提供方案~~~


> github：[https://github.com/skenoy/smartanalysis](https://github.com/skenoy/smartanalysis)
> 
> 本文地址：[https://github.com/skenoy/smartanalysis/instance/mutiprocessing](https://github.com/skenoy/smartanalysis/instance/mutiprocessing)

