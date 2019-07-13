## 来玩玩微信吧（1）————简单分析好友

手机微信就不说了，大家都用的比较6了，怎么自动化操作微信的内容呢？比如看看所有好友的情况，比如查看好友撤回的消息，比如群发过年祝福消息，比如做个自动回复机器人，比如陪男友（女友）智能聊天。。。总的来说，对于懒人来讲都有些许遗憾和不足。

幸好微信保留了网页端，那么我们抓取网页返回的消息就可以操作所有的内容了！

目前`python`操作微信比较好的模块是`itchat`，当然基于`itchat`开发出了其他整合的模块，比如`wxpy`等，可以做的事情很多啦！具体使用方法可以查看相关模块的文档即可实现。

那么我们简单来看看`itchat`能做些什么吧！

```python
import itchat

# 短时间关闭程序后重连 hotReload
# 命令行显示二维码 enableCmdQR，如果不用会自动跳出来图片
itchat.auto_login(hotReload=True, enableCmdQR=1)

friends = itchat.get_friends(update=True)

# 查看一下存了一些什么内容
print(friends[0])
# 第一个是自己，顺便查看一下方法有哪些
print([x for x in dir(friends[0]) if not x.count('__')])

sex = {1: 0, 2: 0, 0: 0}
for i in friends[1:]:
    s = i["Sex"]
    sex[s] += 1

total = len(friends[1:])

print(f'总人数：{total}')
print(f'男性：{sex[1]}')
print(f'女性：{sex[2]}')
print(f'其他：{sex[0]}')
```

查看了一下`friends`里面的内容包括很多，比如地址，昵称，签名，备注名等等，发现了很多有意思的东西。

接下来我们来群发消息吧！~

```python
import time

friendList = itchat.get_friends(update=True)
for friend in friendList[1:]:
    name = friend["DisplayName"] or friend['NickName']
    # 为了大家不会直接运行发送，这是打印出来的。。。发送使用 itchat.send替换print即可
    print(f"祝 {name} 新年快乐！{friendList[0]['NickName']}")
    time.sleep(.5)
```

为什么不能群发群聊？是因为网页端和手机端的群聊信息不是完全同步的，如果想发群聊信息，那么你必须先保存群聊到你的通讯录才能发送！！！

那怎么得到群聊信息呢？很简单，`itchat.get_chatrooms(update=True)`即可~~~

那么下次我们找点其他的内容来看看吧~~~


> github：[https://github.com/skenoy/smartanalysis](https://github.com/skenoy/smartanalysis)
> 
> 本文地址：[https://github.com/skenoy/smartanalysis/weixin/weixin/1](https://github.com/skenoy/smartanalysis/weixin/weixin/1)

