## 玩玩进度条吧

在写程序的时候，尤其是循环比较多的时候，总是尴尬的在等待，也不确定什么时候能完成，有时候看着别人写的程序有进度的提醒感觉很安心，虽然说有些不是很准，比如GATK callsnp的时候= =

`python`有个强大的第三方模块————tqdm，解决了我的需求~~~

```python
import tqdm
import time

for i in tqdm.tqdm(range(1000), desc='这是第一步: '):
    time.sleep(0.001)

# trange可以替代range，参数一致
for i in tqdm.trange(1000):
    time.sleep(0.001)
```


我们来看看有意思的参数吧~
`ncols`: 总的进度条长度
`leave`: 进度条完成后是否保留在屏幕上
`ascii`: 更换进度条样式
`unit`: 循环的单位


如果想看测试情况，请到github上下载（该死的公众号把制作的gif给压缩的不能发上来了。。。）


![看不清楚了。。。](https://mmbiz.qpic.cn/mmbiz_gif/mYJibSOraq9rYrUJ9ABgsjyRhfWP1wu9IM8c0KtvgBiaqsld38SJr8rjlIVfI3Y1cqvRziaAxMKPgnkicrOoOqFSbQ/0?wx_fmt=gif)


不仅可以在`python`里面使用，还可以在`linux`环境下使用：
```shell
seq 9999999 | tqdm --bytes | wc -l

find . -name '*.py' -type f -exec cat \{} \; | tqdm | wc -l
```

还能怎么玩？去作者的github吧，来看看更多的玩法！~~~

> github：[https://github.com/skenoy/smartanalysis](https://github.com/skenoy/smartanalysis)
> 
> 本文地址：[https://github.com/skenoy/smartanalysis/instance/tqdm](https://github.com/skenoy/smartanalysis/instance/tqdm)

