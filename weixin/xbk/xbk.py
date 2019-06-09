import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid", {"font.sans-serif": ['simhei', 'Droid Sans Fallback']})


a = pd.read_csv('format.xbk')

dist = a.groupby('prov')['number'].agg(sum).sort_values(ascending=False)
plt.figure(figsize=[6,6])
sns.barplot(x=dist.values, y=dist.index, palette='BuGn_r', orient='h')
#plt.xticks(rotation=90)
plt.ylabel("省份")
plt.savefig('shenghuiCount.png', dpi=200, bbox_inches='tight')


from pyecharts.charts import Map
from pyecharts import options as opts
m = Map()
m.add("", [list(z) for z in zip(list(dist.index), list(dist.values))], 'china')\
    .set_global_opts(visualmap_opts=opts.VisualMapOpts(max_=800,range_color=["lightskyblue", "yellow", "orangered"]))
m.render('shenghuiHM.html')


mr = a[a.ranks<=3]
mr.ranks = mr.ranks.astype(int)
plt.figure(figsize=[6,8])
sns.catplot(x='number',y='city', hue='capital', data=mr, row='ranks', kind='bar', orient='h', sharey=False)
plt.savefig('shenghuiSUM.png', dpi=200, bbox_inches='tight')
