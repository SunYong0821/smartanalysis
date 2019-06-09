# coding=utf-8
import requests, re
from lxml import etree

url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018'
html = requests.get(f"{url}/index.html",
                    headers={
                        'user-agent': "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"})
if html.status_code == 200:
    html.encoding = 'gb2312'
select = etree.HTML(html.text)
pro = select.xpath("//tr[@class='provincetr']//td/a/text()")
surl = select.xpath("//tr[@class='provincetr']//td/a/@href")
for i, v in enumerate(pro):
    if v.count('市'):
        v = v.replace('市', '')
        print(v + '\t' + v)
    else:
        v = v.replace('省', '').replace('自治区', '').replace('回族', '').replace('壮族', '').replace('维吾尔', '')
        shtml = requests.get(f'{url}/{surl[i]}',
                             headers={
                                 'user-agent': "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"})
        if shtml.status_code == 200:
            shtml.encoding = 'gb2312'
        s = etree.HTML(shtml.text)
        city = s.xpath("//tr[@class='citytr']//td[2]/a/text()")
        city = [re.sub(r'市|盟|自治州|地区', '', c) for c in city if not re.search(r'行政区', c)]
        for c in city:
            print(c + '\t' + v)
