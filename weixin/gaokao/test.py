import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']

f = pd.read_csv('0.csv', encoding = "gbk")
fig, ax1 = plt.subplots()
sns.lineplot(x='年份', y='理一本', data=f,label='理一本', ax=ax1)
sns.lineplot(x='年份', y='理二本', data=f,label='理二本', ax=ax1)
sns.lineplot(x='年份', y='文一本', data=f,label='文一本', ax=ax1)
sns.lineplot(x='年份', y='文二本', data=f,label='文二本', ax=ax1)
plt.ylabel('二本以上')
ax2 = ax1.twinx() 
sns.lineplot(x='年份', y='报考（万）', data=f, label='报考（万）', color='gray', ax=ax2)
plt.savefig('1.png', dpi=250, bbox_inches='tight')