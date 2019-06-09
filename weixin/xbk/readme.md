### 开搞
> 看本篇文章基础：python、html

在写第一篇分析的时候，`落雨无声`我这位朋友说数据很简单，随便来抓就行了，我就这样欣然地跑到官网查了一下发现数据不对，怎么不对？我记得kaggle有这个2017年的数据，一对比发现错了好几倍。。。这就尴尬了，怎么办？虽说人工智能很NB，但首先也得是人工（*标注*）吧，所以这位朋友吭哧吭哧把地图看了一遍，然后眼瞎了。。。

开个玩笑，朋友的毅力值得表扬（doge脸）。整理好的数据在`format.xbk`文件内敬请查阅，抓取时间是5月28日。

|city  |  prov  |  number|capital|ranks|
|:-:|:--:|:--:|:--:|:--:|
|上海	|上海	|751|1|1|
|台湾	|台湾	|481|1|NaN|
|北京	|北京	|331|1|1|
|杭州	|浙江	|253|1|2|

##### 分别为城市、省份、数量、是否是省会与某刚发布的排名

[http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/index.html](http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/index.html) 省会那么简单，就不用劳烦眼力了。。。查之前记得先看看`robots.txt`，看看网站让不让人爬，这是规范的第一步，结果ZF的网站居然没有这个，那就随便了= =

```python
# coding=utf-8
import requests, re
from lxml import etree
url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018'
html = requests.get(f"{url}/index.html",headers={'user-agent': "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"})
# 中文网页需设置编码，查看网页head可以知道编码所在
if html.status_code == 200:
    html.encoding = 'gb2312'
select = etree.HTML(html.text)
# lxml语法，网上随便搜，常用的没几个
pro = select.xpath("//tr[@class='provincetr']//td/a/text()")
surl = select.xpath("//tr[@class='provincetr']//td/a/@href")
```
以上把主要的代码用注释标识一下，详看`github`中的程序`getProvinceCity.py`

先吐槽一下网上的教程吧，实在是看不下去，到现在我的学习库中还有几种不同的写法。。。
> 请用requests库，放弃使用urllib2等，使用方法尤其复杂；
> 请用lxml库，放弃beautifulsoap库，速度太慢了；
> headers可以在网上收集一些，防止被屏蔽，当然还有其他方面要防止屏蔽的，比如ip使用代理、登陆需要cookie等等；

爬下来之后就要统计作图了，这里使用了`seaborn`库，至于`matplotlib`库个性化设置的时候看看就可以了。`seaborn`库有段时间我想把整个**生物信息流程**的图都给重画一遍，整体看起来就漂亮许多，可是比较懒。。。

`pandas`是后续统计的重要库，说实话比`R`的操作好用很多，用好了数据分析师就是囊中之物。

有什么问题，可以发信息给这个公众号或者去`github`上提个`issue`吧

> https://github.com/skenoy/smartanalysis/tree/master/weixin/xbk

![]()

![](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9pLEwFgUObcImwB175s3Nm5eXowgRhE68Nq10K66oBpHiblP6L9XicpeKs9vqUp6NqrYoypNqP37rTA/0?wx_fmt=png)