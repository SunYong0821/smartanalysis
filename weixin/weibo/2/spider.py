# coding=utf-8

import requests
import re
import time

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'cookie': "SCF=ArXirfRW-SLeH3lH7kdh4X7ToTBoAWfNySAkVESlPZgMHo198XF8errgcB1_V96KzCKyhePznMp9GI4QWOra6yU.; ALF=1562675739; SUB=_2A25wFMx6DeRhGedI71YR8izOwjyIHXVT9tQyrDV6PUJbkdAKLVDbkW1NV3AGExXf5r5YAcVbfG5XdG91o8oeJ7Fu; SUHB=0C1Dr2neQkRzSX; MLOGIN=1; _T_WM=96372004017; WEIBOCN_FROM=1110006030; XSRF-TOKEN=ccb1b4; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803%26uicode%3D20000174"}


def getComment(num):
    data = requests.get(
        f'https://m.weibo.cn/api/comments/show?id=4386261885948066&page={str(num)}', headers=header)
    if data.status_code == 200:
        return data.json()
    return False


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


if __name__ == '__main__':
    ostr = ''
    for i in range(100):
        time.sleep(1)
        cm = getComment(i + 1)
        if cm is False:
            continue
        ostr += parseComment(cm)
    with open('comment.csv', 'w', encoding='utf-8') as of:
        of.write(ostr)