## 抓取微博评论/转发信息（2）

上篇我们讲了评论/转发的抓取机制，发现评论其实只能抓取100页，但是转发能抓取**全部**哦！
> 抓取转发时要注意页数并不能从json数据中得到，且每页的个数并不是固定的10条（有可能被官方给屏蔽了），有可能会多哦~
> 另外转发得到的信息要比评论多很多，比如客户端，关注数、粉丝数等等信息，为了简单起见暂时只关注评论抓取

那我们就开始了！首先还是开始构造我们的抓取结构：

```python
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
          'cookie': "XXXXXXXXX"}

def getComment(num):
    data = requests.get(
        f'https://m.weibo.cn/api/comments/show?id=4386261885948066&page={str(num)}', headers=header)
    if data.status_code == 200:
        return data.json()
    return False
```

上篇我们说了必须使用`cookie`才能爬取，所以我们必须先登陆获取cookie，然后打印出来测试一下：

![报错了？？？](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9oEDnpwukZmfRtFVbhZ2qhEVZ4VLA8Dib8vusKh0q7Ru8uM1FACBIXGQbRezXMsCuo0RsbvrNyYqDg/0?wx_fmt=png)

怎么回事？怎么会出这个问题？经过长久的测试，发现是`anaconda`的SSL证书和`python`的SSL证书不一致导致的。。。网上很多解决方法，什么加入环境变量啊，什么重新安装`openssl`啊，在我这里都不可用。。。真是麻烦的要死。。。之前能用是因为用的另外一台电脑。。。怎么解决呢？卸载`anaconda`，重新独立安装`python`和`anaconda`即可。

我们看一下需要什么内容：

![返回json内容](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9oEDnpwukZmfRtFVbhZ2qhEYQS6k44hiaAvXkNlI6YOxhNNrsicSBOpRKNuhcQCVRWOPgI5iaZrspMgA/0?wx_fmt=png)

简单获取评论人的昵称、粉丝数和回复内容：

```python
def parseComment(jf):
    pageout = []
    for i in jf['data']['data']:
        text = re.sub(r'<.*>|回复<.*>:|转发微博', '', i['text'])
        if text and text != '。':
            pageout.append(f"{i['user']['screen_name']},{i['user']['followers_count']},{text}")
        else:
            pageout.append(f"{i['user']['screen_name']},{i['user']['followers_count']},None")
    out = '\n'.join(pageout)
    return out
```

把一些不相干的内容替换掉并把没有内容的设置成想要的占位符即可，最后输入到文件内即可。

由于部分页面可能被官方给屏蔽了，所以我们要确认一下内容是否存在，完整的代码已上传到github上，任取~~~

> github：[https://github.com/skenoy/smartanalysis](https://github.com/skenoy/smartanalysis)
> 本文地址：[https://github.com/skenoy/smartanalysis/weibo/2](https://github.com/skenoy/smartanalysis/weixin/weibo/2)


