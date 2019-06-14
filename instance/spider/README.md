## 关于爬虫

对于**生物信息**来说，爬虫并没有太大的用处，只是偶尔用得到（比如爬KEGG，自动化查询NCBI等等）；对于数据分析来说，爬虫重要性增加了很多，毕竟很多数据来源很复杂。

简单讲点`python`爬虫吧，实用为主。

### 检查`robots.txt`
Robots协议也称作爬虫协议（网络爬虫排除标准，Robots Exclusion Protocol），用来告诉爬虫和搜索引擎哪些页面可以抓取。`robots.txt`文件一般放在网站的根目录下。
```
User-agent: *
Disallow: /
Allow: /public/
```
看看就明白哪些允许爬了，如果网站没有，那就随便吧。看这个的目的就是防止法律风险，当然也有打擦边球的。。。

### 爬虫学习路径
总结一下学习路径：

![](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9qTssWlI3zQMJiaUL6K7qasdAWUgJhZS81Cm1MP8RBfLSiaibevQmRS8TFj9X7LHIZQjjZiagFPUVuBcg/0?wx_fmt=png)

- 据说pyppeteer可以替代Selenium+PhantomJS组合。
- 左侧路径有框架`Scrapy`，不过基本请求和解析方法没有变化，百万级爬虫请使用框架吧，但对于生物信息分析来说基本用不到，数据分析大多数情况也很难用到。
- 我找了一些header仅供参考，详见github下instance/spider/header.txt
- 代理IP，这个网站不错: https://www.xicidaili.com/nn
- 反爬虫策略使用方法：
```python
# F12检查浏览器中的cookie内容
header = {
    'user-agent': 'XXX',
    'cookie': 'XXX'}
}
requests.get("https://name", headers=header, proxies={'http': 'XXX:OOO'})
```

### 还有什么没考虑到
再详细点就是`requests`的`post`和`session`等等，另外就是多线程和异步处理加速运行；目的不同，学习程度也不同，只要一段时间内适合自己即可。

> 公众号爬虫的目的大多数为朋友们进行数据分析所用，所以代码复用率会很高，第一次就详细写，其他时候就简单提几句。

![]()

![](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9pLEwFgUObcImwB175s3Nm5eXowgRhE68Nq10K66oBpHiblP6L9XicpeKs9vqUp6NqrYoypNqP37rTA/0?wx_fmt=png)