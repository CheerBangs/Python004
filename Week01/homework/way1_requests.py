# 爬取猫眼电影的前 10 个电影名称、电影类型和上映时间
# 1. 首页href 2. 详情页获取具体信息
import requests
from bs4 import BeautifulSoup as bs
import time
import pandas

maoyanUrl = 'https://maoyan.com/films/?showType=3'
localMaoyanUrl = 'http://localhost:8080/maoyan.htm'
localMaoyanDetailUrl = 'http://localhost:8080/detail.htm'
mockHeader = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.3'
}


def fetchHome(url):
    r = requests.get(url, headers=mockHeader)
    bsInfo = bs(r.text, 'html.parser')
    count = 0
    allInfo = []
    for domA in bsInfo.find_all('a', attrs={'data-act': 'movies-click'}):
        if count < 10:
            count = count + 1
            detailUrl = domA.get('href')
            print(detailUrl)
            allInfo.append(fetchDetail(localMaoyanUrl))
            # allInfo.append(fetchDetail(localMaoyanDetailUrl))
            time.sleep(2)
    save(allInfo)

def fetchDetail(detailUrl):
    detailResult = requests.get(detailUrl, headers=mockHeader)
    bsInfo = bs(detailResult.text, 'html.parser')
    containerClass = '.movie-brief-container '
    mainInfo = {
      'title': bsInfo.select_one(containerClass + 'h1').get_text(),
      'type': ''.join([domA.get_text() for domA in bsInfo.select(containerClass + '.text-link')]),
      'time': bsInfo.select(containerClass + 'li')[2].get_text()
    }

    print(mainInfo)
    return mainInfo

def save(content):
  pand = pandas.DataFrame(content)
  pand.to_csv("./movie.csv", sep="，", encoding="utf8", index=False, header=False)

fetchHome(maoyanUrl)
# fetchHome(localMaoyanUrl)