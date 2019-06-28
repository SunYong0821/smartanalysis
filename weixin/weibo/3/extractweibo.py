# coding=utf-8

import requests
import re
from multiprocessing import Pool
import time
import random

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'cookie': "ALF=1563689512; WEIBOCN_FROM=1110106030; _T_WM=60719391204; MLOGIN=1; SCF=Arn4Ssh7aVKMntNiQBkf3NkQkLtOwzcGauLBuCyK6mplGbM00epwc1kyvfu8AkbmPPLGqwdr43uKUJY00Ml8N9g.; SUB=_2A25wERdBDeRhGedI71YR8izOwjyIHXVT_bkJrDV6PUJbktAKLUPdkW1NV3AGEwCEZDv-D5Q6gXUAOPDTuSQaNVGD; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5ExQ6lnrd1W5MGZ_UzwEWI5JpX5K-hUgL.Fo2cShB7eozE1K52dJLoI0YLxKnLB.qLB.BLxK-L1-zL1--LxK.L1h5L1-BLxK-L12-LB.zLxKML1-2L1hBLxK-L12BL1h2LxK-LBo.LBoBt; SUHB=0pHw__nxccVhQa; SSOLoginState=1561683729; M_WEIBOCN_PARAMS=oid%3D4387818392289541%26luicode%3D20000061%26lfid%3D4387818392289541; XSRF-TOKEN=d57dbe"}


def randomip():
    rr = random.randint(1, 100)
    with open('ip.txt') as ip:
        m = 1
        for ii in ip:
            m += 1
            if rr == m:
                k, v = ii.strip().split(',')
                return {k: v}


def getRepost(num):
    time.sleep(random.randint(5, 10))
    # rip = randomip()
    # data = requests.get(
    #    f'https://m.weibo.cn/api/statuses/repostTimeline?id=4387818392289541&page={str(num)}', headers=header,
    #    proxies=rip)
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


if __name__ == '__main__':
    p = Pool(5)
    results = []
    for i in range(1200):
        n = i + 1
        results.append(p.apply_async(getRepost, (n,)))
    with open('comment.csv', 'w', encoding='utf-8') as of:
        for i in results:
            if i.get():
                of.write(i.get() + '\n')
    p.close()
    p.join()
