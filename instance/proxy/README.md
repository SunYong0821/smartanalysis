## 获取有效代理
代理这个挺重要的，所以将上篇文章的代理给爬下来，作为以后ip池，说干就干！

首先检查一下`robots.txt`，发现全部禁止！。。。本文结束！！！

。。。

尴尬！虽然不让爬吧，人工复制第一页也就足够了，就是处理比较麻烦。所以还是爬吧，只爬一页做个示例。

首先用`chrome`浏览器打开目标网址，按`F12`打开调试模式然后刷新一下
![根据箭头找到返回对象](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9qNFA6IZ2ocFHS9uKp3DPcmaWmxIYDqia8OyASatNyUQHuNGNSutCqz5ib20QJByGKtEticeZSZtyOgg/0?wx_fmt=png)

发现返回是`text`对象，那么就直接lxml处理了：
```python
def getProxy():
    # getHeader()随机得到一个header
    header = getHeader()
    html = requests.get('https://www.xicidaili.com/nn', headers=header)
    html = etree.HTML(html.text)
    # 找到我们想要的内容
    ip = html.xpath('//tr/td[2]/text()')
    port = html.xpath('//tr/td[3]/text()')
    http = html.xpath('//tr/td[6]/text()')
```

虽然只爬一页，但是每个ip需要测试是否有效，想了一下，用多线程处理比较好，结果发现所有的线程池模块都不是很好用，最好用的是`concurrent.futures`。之前说了web端处理用线程消耗资源是最少的，但是这些模块也太难用了。。。偶然间发现了一个新的线程池模块--`vthread`，试了一下感觉还不错：
```python
@vthread.pool(8)
def testProxy(header, proxy, out):
    testip = requests.get('http://www.baidu.com',
                          headers=header, proxies=proxy)
    if testip.status_code == 200:
        q.put(out)
```
> 需要注意的是，该模块没有返回值，暂时只能用`queue`来获取，且结果的顺序跟线程运行的顺序一致（想办法把结果输入到队列中去）
> 以上仍然有个问题，就是队列的数量需跟循环次数一致，否则无法输出

这两步处理完之后，基本其他没什么难度了，完整代码如下：
```python
# coding=utf8

import random
import requests
from lxml import etree
import vthread
import queue

q = queue.Queue()


def getHeader():
    headers = ["Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
               "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
               "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
               "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
               "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
               "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
               "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
               "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
               "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
               "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
               "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
               "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
               "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
               "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
               "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
               "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
               "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
               "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
               "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
               "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
               "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
               "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
               "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
               "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
               "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
               "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
               "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"]
    return {'user-agent': random.choice(headers)}


def getProxy():
    header = getHeader()
    html = requests.get('https://www.xicidaili.com/nn', headers=header)
    html = etree.HTML(html.text)
    ip = html.xpath('//tr/td[2]/text()')
    port = html.xpath('//tr/td[3]/text()')
    http = html.xpath('//tr/td[6]/text()')
    for a, b, c in zip(ip, port, http):
        h = getHeader()
        p = {c: a+':'+b}
        testProxy(h, p, f'{c},{a}:{b}\n')
    return len(ip)


@vthread.pool(8)
def testProxy(header, proxy, out):
    testip = requests.get('http://www.baidu.com',
                          headers=header, proxies=proxy)
    if testip.status_code == 200:
        q.put(out)


if __name__ == '__main__':
    number = getProxy()
    with open('ip.txt', 'w') as ipfile:
        for i in range(number):
            ipfile.write(q.get())

```

这样每次在爬目标内容前，运行一遍就可以了~

> 所有文章地址在github: https://github.com/skenoy/smartanalysis

![](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9pLEwFgUObcImwB175s3Nm5eXowgRhE68Nq10K66oBpHiblP6L9XicpeKs9vqUp6NqrYoypNqP37rTA/0?wx_fmt=png)