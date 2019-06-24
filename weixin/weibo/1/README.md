## 最新抓取微博评论/转发信息（1）

抓取微博评论和转发信息正常方法来讲还是比较难的，但是一般网站都有其他途径获取相关内容。

很早之前微博评论抓取的方法是用移动端的微博：
![移动端微博](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9oz2sPCHhuOsmnTFjicfJyvY2MTkeJeQrD7PrVicf742mYDKPCkkc9cWZiawlzycMbsKj93bZePUmyCw/0?wx_fmt=png)

然后直接找到相关微博，点击得到评论的id即可：
![最新移动端微博](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9oz2sPCHhuOsmnTFjicfJyvYR6NPia8T5Tkfq6xKbS2ZEvSrx8JS7jFKhyDf6ZspLdFqsyEmFZ5Fztw/0?wx_fmt=png)

然后使用以下`api`获取评论信息（（转发也是同样的道理））：
> https://m.weibo.cn/api/comments/show?id=xxxxxxxx&page=1
> 转发`api` https://m.weibo.cn/api/statuses/repostTimeline?id=xxxxxxxx&page=1

返回的结果是json格式，如下：
![返回信息](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9oz2sPCHhuOsmnTFjicfJyvY8aSQ0B0PaNhGuA8OGQY1icbqTUvPBR8Lgib3JKLQzBmOUvYYdfG4doDQ/0?wx_fmt=png)

所以简单来讲，我们使用相关api即可获取我们想要的内容，但时间长了就不一定了，因为很可能会被封掉。

另外一个问题，这种方法只能抓取100页的评论，超过了就不能获得内容了，随便找了一条微博评论很多：
![第100页内容](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9oz2sPCHhuOsmnTFjicfJyvYXD8KAQRHG2fK5cgAQYvLbj0bZgv6zxOtk3p6b5BcysaDcC9TZFJaBg/0?wx_fmt=png)

我们发现总条数是1W多，1K页，但是只能抓100。。。设置的可真好。。。
![没有数据了。。。](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9oz2sPCHhuOsmnTFjicfJyvYHxZunf8ootcJtSrCH4Wc3dhicqcwhF0c8bIUfiagaBynDnZxGrIRklnw/0?wx_fmt=png)

有没有完整的办法，有！模拟浏览器进行抓取！这个就算了。。。

> 以上信息是在登陆的情况下完成，所以在写程序抓取的时候带上cookies哦，下篇再说

> github：[https://github.com/skenoy/smartanalysis](https://github.com/skenoy/smartanalysis)
> 本文地址：[https://github.com/skenoy/smartanalysis/weibo/1](https://github.com/skenoy/smartanalysis/weixin/weibo/1)


