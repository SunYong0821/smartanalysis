## 生信领域用Python替代R的分析——生存分析

有人在后台留言说，干嘛不讲点生物信息的，是不是本末倒置了？你说Python要兴起，那是基于人工智能，怎么可能替代`perl`和`R`，比如生存分析就替代不了。。。

对此，我可是没说过替代之类的“悖逆”之言，╮（╯＿╰）╭，只是说学习成本低，语言严谨，没有那么花哨，理解起来容易而已，更重要的是对新人比较友好。。。我敢说我有时候都看不懂我带的人写的`perl`代码。。。至于`R`，速度太慢，数据结构真难理解。。。

至于某些分析确实网络上`python`讲的不多，不过不是没有，只是少见而已，生存分析也是有的~（如果对生存分析不了解，请百度~这里不讲解原理了~）

先来做个对比：
```R
library(survival)
mat <- read.table('clinical.txt', header=T, sep="\t", check.names=F)
mat$futime = mat$futime / 365 # month~30
out <- data.frame()

for(i in colnames(mat[, 4:ncol(mat)])){
    md <- mat[, i] < median(mat[, i])
    diff <- survdiff(Surv(futime, fustat)~md, data=mat)
    pValue <- 1 - pchisq(diff$chisq, df=1)
    out <- rbind(out, cbind(gene=i, pvalue=pValue))
    pValue <- signif(pValue, 4)
    pValue <- format(pValue, scientific=TRUE)

    fit <- survfit(Surv(futime, fustat)~md, data=mat)
    summary(fit)

    png(paste(i, ".survival.png", sep=""))
    plot(fit, lwd=2, col=c("red", "blue"), xlab="Time (Year)", mark.Time=TRUE, main=paste("Survival curve (p=", pValue, ")", sep=""))
    legend("topright", c(paste(i, " high expression", sep=""), paste(i, " low expression", sep="")), lwd=2, col=c("red", "blue"))
    dev.off()
}
write.table(out, file="survival.xls", sep="\t", row.names=FALSE, quote=FALSE)
```

以上代码是计算高表达和低表达基因的生存分析，使用的是`survival`包，诸君可随意拿来使用~


我们来看一下`Python`中的`lifelines`模块吧！

```python
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
import pandas as pd
import matplotlib.pyplot as plt
f = pd.read_csv('b.csv')
km = KaplanMeierFitter()
T = f['futime'] / 365
E = f['fustat']
km.fit(T, event_observed=E)
km.plot()
```

![KM分析](https://mp.weixin.qq.com/cgi-bin/filepage?type=2&begin=0&count=12&group_id=102&view=1&token=427725270&lang=zh_CN)

简单几步就完成了整体的生存分析，那么比较怎么做呢？

```python
gender = (f['gender'] == 'MALE')
ax = plt.subplot(111)
km.fit(T[gender], event_observed=E[gender], label="Male")
km.plot(ax=ax)
km.fit(T[~gender], event_observed=E[~gender], label="Female")
km.plot(ax=ax)

lr = logrank_test(T[gender], T[~gender], E[gender], E[~gender], alpha=.99)
print(lr.p_value)
```
![KM比较](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9oeRXG3U9OkPBjDZzkzlvvVhR3WhiaXicZ3oPFibktPEgdxWSVbkwm7Hk0GokTVEjjrPlZ1hMZcBDnVA/0?wx_fmt=png)

这样我们就得到了P值和比较图了~

当然我也是测试了好几个模块，通过不同的比较发现`lifelines`这个模块封装的最好，用起来最简单，最重要的是可以完美兼容`pandas`和`sklearn`结构，使用起来非常方便！

PS：我把输入也上传了，大家可以随意查看格式内容~请到github上下载~

> github：[https://github.com/skenoy/smartanalysis](https://github.com/skenoy/smartanalysis)
> 
> 本文地址：[https://github.com/skenoy/smartanalysis/instance/survival](https://github.com/skenoy/smartanalysis/instance/survival)

