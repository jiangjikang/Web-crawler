# -*- coding: UTF-8 -*-
"""
@Project ：pythonProject 
@File    ：getHTML.py
@Author  ：蒋继康
@Date    ：2022/4/9 13:19 
"""

import urllib.request
import re
from bs4 import BeautifulSoup

url = "https://movie.douban.com/top250?start="


def main():
    getData(url)


findLink = re.compile(r'<a href="(.*?)">')  # 影片链接
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # 影片图片
findTitle = re.compile(r'<span class="title">(.*)</span>')  # 影片片名
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')  # 影片评分
findJudge = re.compile(r'<span>(\d*)人评价</span>')  # 影片评价人数
findInq = re.compile(r'<span class="inq">(.*)</span>')  # 影片概述
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)  # 相关影片


# 爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0, 2):
        url = baseurl + str(i * 25)
        html = getURL(url)

        bs = BeautifulSoup(html, "html.parser")

        for itme in bs.find_all('div', class_="item"):
            data = []
            itme = str(itme)

            link = re.findall(findLink, itme)[0]
            data.append(link)

            imgSrc = re.findall(findImgSrc, itme)[0]
            data.append(imgSrc)

            titles = re.findall(findTitle, itme)[0]
            if (len(titles) == 2):
                data.append(titles[0])
                data.append(titles[1].replace("/", ""))
            else:
                data.append(titles[0])
                data.append(' ')

            Rating = re.findall(findRating, itme)[0]
            data.append(Rating)
            Judge = re.findall(findJudge, itme)[0]
            data.append(Judge)

            Inq = re.findall(findInq, itme)
            if len(Inq) != 0:
                data.append(Inq)
            else:
                data.append(" ")

            bd = re.findall(findBd, itme)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)
            # bd = re.sub('/', " ", bd)
            data.append(bd.strip())
            datalist.append(data)
    print(datalist)
    return datalist


# 获取指定的网页内容
def getURL(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15",
        "X-Amzn-Trace-Id": "Root=1-625118d0-6c419c1b6ae518ca3696485b"
    }
    try:
        response = urllib.request.urlopen(urllib.request.Request(url=url, headers=headers))
        return response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print("连接失败")
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)


if __name__ == "__main__":
    main()
