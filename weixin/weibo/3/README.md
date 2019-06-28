## 昨天的微博服务器又崩溃了。。。爬？分析？

昨天的微博服务器又崩溃了。。。吃瓜群众又有新的*多个瓜*可吃了，但本文却不是对弄崩服务器的*瓜*进行分析，而是对昨天的**18岁结婚建议**进行挖掘。

打开该微博的源头，跟之前一样进行移动端的爬虫处理，由于我们知道评论是有可能被关的，而且只能爬100页，所以我们对转发信息进行抓取。

![看看目前多少页](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9ofkMN5wQfhEibms8vyuBTuAzrgduibDm8tJWY5icwOHkpwvnksbEAq8mwkXKWYiaPDzD1nicvTQQjk8nw/0?wx_fmt=png)

所以就简单的按照之前的进行爬取，不过在爬取的过程中遇到了`HTTP 418`错误。。。居然遇到了反爬技术，随后对`header`、`ip`、多进程做了处理，发现还是不行。。。怒了！加上随机睡眠及递归处理！终于可以慢慢爬取了。。。时间有点慢，没办法喽！顺便问一句大佬们除了用js的方法之外，还有其他方法可以顺利爬取吗？核心代码如下，请指教：

```python
def getRepost(num):
    time.sleep(random.randint(5, 10))
    data = requests.get(f'https://m.weibo.cn/api/statuses/repostTimeline?id=4387818392289541&page={str(num)}',
                        headers=header)
    print(num)
    if data.status_code == 200:
        jf = data.json()
        pageout = []
        for i in jf['data']['data']:
            text = re.sub(r'<.*>|回复<.*>:|转发微博|//', '', i['text'])
            if all([text, text != '。', text != '，']):
                pageout.append(
                    f"{i['user']['screen_name']},{i['user']['followers_count']},{i['user']['follow_count']},{text}, "
                    f"{i['source']}, {i['user']['gender']}")
            else:
                pageout.append(
                    f"{i['user']['screen_name']},{i['user']['followers_count']},{i['user']['follow_count']},None, "
                    f"{i['source']}, {i['user']['gender']}")
        out = '\n'.join(pageout)
        return out
    else:
        time.sleep(10)
        getRepost(num)
```

## 来做一下数据分析吧
经过两个小时完成下载，但由于微博是动态更新的和部分信息会被屏蔽，所以总的数据并没有我们看到的那么多，去重之后共计9217条数据，去重方法如下：

> cat <(head -1 repost.csv) <(le repost.csv  | sed 1d | sort -k 1,1 -k 4,4 | uniq) > repost.uniq.csv

但并不是每条数据都有有效信息，所以我从两个方面进行分析。

### 词云分析

首先进行词云频率分析，结果如下：

![词云图](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9ofkMN5wQfhEibms8vyuBTuAtiauLAA9D1ckyEvLOMicpu1AKRibQvuNIcJsMQeVwD0ot6HD5azCXf4HA/0?wx_fmt=png)

分词之后的结果可以看到，争议集中在*孩子*，*年龄*、*教育*等方面，当然也有不满意的地方，比如*韭菜*。。。*房价*。。。等等。不过，大家都想的那么长远吗？
居然说到*高考*，甚至*加分*？我倒是觉得*责任*，*担当*应该是首先考虑的吧。。。不过对*砖家*真是毫不留情，不细说了。。。

### 情感分析
然后我们使用`SNOWNLP`模块对每条信息进行情感分析，简单分为`积极`、`中性`和`消极`三个方面，并且把手机按照品牌设置了分类，最终得到了7812条有效数据。核心代码如下：

```python
fenci = []
with open('repost.uniq.csv', encoding='utf-8') as f, open('out.sentiments.csv', 'w', encoding='utf-8') as out:
    rr = re.compile(r'^…|:|text|？|，|。|...|\s|《|》|！|\?|a|in')
    stopwords = stopwordslist()
    for i in f:
        eles = i.strip().split(',')
        if eles[3] != 'None':
            sentiment = SnowNLP(eles[3])
            if sentiment.sentiments > 0.66:
                out.write(f'积极,{eles[4].strip()},{eles[5]}\n')
            elif sentiment.sentiments < 0.33:
                out.write(f'消极,{eles[4].strip()},{eles[5]}\n')
            else:
                out.write(f'中性,{eles[4].strip()},{eles[5]}\n')
            for j in jieba.cut(eles[3]):
                if not rr.search(j) and j not in stopwords:
                    fenci.append(j)
num = Counter(fenci)
wc = WordCloud(font_path="simhei.ttf", background_color="white", max_words=100, width=1000, height=860, margin=2)
wc.generate_from_frequencies(num)
plt.axis("off")
wc.to_file('test.png')
```

详见`out.sentiments.csv`文件，接下来看看统计结果吧：

![统计表](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9ofkMN5wQfhEibms8vyuBTuAob1tsdo58TXYq1bxZTTSkcHq6A6y9IoVntGbFjkQ1ywIjD1yxc1R5Q/0?wx_fmt=png)

![居然积极的信息最多](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9ofkMN5wQfhEibms8vyuBTuAuADdF8HFvzgZtKZoia4enT9JSicuee2WyemsZ0sxpTq1Yx1oxVman3uw/0?wx_fmt=png)

感觉有点问题，需要查看这些积极的信息内容是否真的是积极，不详细说了。

![iphone是一直独秀啊](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9ofkMN5wQfhEibms8vyuBTuAyp0p9RtQo1adL1Yvm68ehBQBM4U6H5ZEdcX4lA8AA4GOT62aS7mm5w/0?wx_fmt=png)

iphone是一直独秀啊，如果荣耀和华为合并到是能达到iphone的一半了，另外有400多条数据完全不知所谓，比如xx后援会，无意义的话等等。

![女性用户占绝大多数](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9ofkMN5wQfhEibms8vyuBTuAkqlI25X2e0Ziaqp9P6MfJPpj8b5rkQ8QxbUNLukY8wfKujfefsFnPlQ/0?wx_fmt=png)

女性用户占绝大多数，感觉不合情理啊，除非是微博默认的性别是女的，毕竟懒人占大多数。也有这个可能，女性更关注这个话题，然而我想起来某次抽奖只有一个男的事情，这个不能多说了。。。

至于两个维度关联分析就不做了，因为这个积极的信息占了绝大多数，基本没有什么可解释的。。。可能的原因是`snownlp`模块分析的可能不大准确，或许应该找一下其他模块试试。

![示例，其他关联差不多一样](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9ofkMN5wQfhEibms8vyuBTuAwDUic8ib8YR1KtiawanLRxt7QSTIcW1lhCR92BRgQzOSdOCy72iclyl3gg/0?wx_fmt=png)


> github：[https://github.com/skenoy/smartanalysis](https://github.com/skenoy/smartanalysis)
> 
> 本文地址：[https://github.com/skenoy/smartanalysis/weibo/3](https://github.com/skenoy/smartanalysis/weixin/weibo/3)

