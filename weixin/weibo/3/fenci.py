import jieba
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from snownlp import SnowNLP


def stopwordslist():
    stopwords = [line.strip() for line in open('stopwords.txt', encoding='UTF-8').readlines()]
    return stopwords


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
