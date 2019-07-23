## Python可视化生信领域的静态图

在生物信息领域，我们最常用的就是`R`中的`ggplot2`包和基础绘图包，偶尔比较复杂的时候我们也会用`perl`里的`SVG`包进行定制化绘图，当然也有一些特殊的包绘制特殊的图像，比如`circos`，`共线性`图等等，但万变不离其宗，如果用的6的话，其实基础包能画所有的图像，只不过麻烦与简单相比而已。

那么在`Python`里面最常用的包是什么呢？我们先看看静态图像吧~

首推`matplotlib`，其相当于`R`中的基础绘图工具和高级绘图工具的集合体，但是用起来非常之麻烦，记起来也不容易。

那么就有人对此进行了更高级的封装，比如我们今天讲到的`seaborn`，我们不需要了解太多的底层参数，简简单单就可以完成一个流程内大部分的作图。。。我都有冲动使用这个模块重写以前的分析图片了。。。因为美观、标准化、报告整体效果比较好。

至于怎么使用，就不多说了，看链接文档，如果对`Python`稍微了解的话，很容易模仿出来的。

![示例1](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9r4Gyiaso5L70IxrM4ibQsMCCboLy8mckdSeNz6lAcecibahCS5Kyc8kANdNVyvPBCKQcTKLkRLicPJicQ/0?wx_fmt=png)

![示例2](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9r4Gyiaso5L70IxrM4ibQsMCCWWnJzkSLafaao7PvcqDa5LMjyTJuMutQJibEkIwDuQcz5tFH6t0trgg/0?wx_fmt=png)

![文档也比较清晰](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9r4Gyiaso5L70IxrM4ibQsMCCpEPol6ibNUhib15ic922x6bHRUwchx57uAnIJ4ClaJF4kicdM4051reUYQ/0?wx_fmt=png)

代码也弄了一个例子：

```python
import pandas as pd
import seaborn as sns
sns.set()

# 导入数据集
df = sns.load_dataset("brain_networks", header=[0, 1, 2], index_col=0)

# 选择网络的子集
used_networks = [1, 5, 6, 7, 8, 12, 13, 17]
used_columns = (df.columns.get_level_values("network")
                          .astype(int)
                          .isin(used_networks))
df = df.loc[:, used_columns]

# 创建分类变量
network_pal = sns.husl_palette(8, s=.45)
network_lut = dict(zip(map(str, used_networks), network_pal))

# 转换关系
networks = df.columns.get_level_values("network")
network_colors = pd.Series(networks, index=df.columns).map(network_lut)

# 绘制图像
sns.clustermap(df.corr(), center=0, cmap="vlag",
               row_colors=network_colors, col_colors=network_colors,
               linewidths=.75, figsize=(13, 13))
```

![上述代码结果](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9r4Gyiaso5L70IxrM4ibQsMCCDicwRC5UzYrwSlZfxtSC10bRb6YMQKcX9vUlsOw0XKc4tgDcaM1buibw/0?wx_fmt=png)

就这么多吧！~

> github：[https://github.com/skenoy/smartanalysis](https://github.com/skenoy/smartanalysis)
> 
> 本文地址：[https://github.com/skenoy/smartanalysis/instance/seaborn](https://github.com/skenoy/smartanalysis/instance/seaborn)

