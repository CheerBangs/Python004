import requests
from bs4 import BeautifulSoup as bs
import lxml.etree
import pandas
import time

maoyanDomain = "https://maoyan.com/"
maoyanUrl = "https://maoyan.com/films?showType=3"
myHeaders = {
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.3'
}

def getInfo(url):
    response = requests.get(url, headers=myHeaders)
    bsInfo = bs(response.text, "html.parser")
    movies = []
    count = 0
    for title_div in bsInfo.find_all("div", attrs={"class": "movie-item-title"}):
        if count < 10:
            movie = {}
            count = count+1
            title_a = title_div.find("a")
            movie_title = title_a.text
            print('hh')

            movie["title"] = movie_title
            movie_detail_href = maoyanDomain + title_a.get("href")
            print(movie_detail_href)
            get_detail(movie_detail_href, movie=movie)
            movies.append(movie)
    save(movies)


def get_detail(url, movie={}):
    time.sleep(2)
    # 电影类型
    movie_types = []
    # 上映日期
    movie_date = ""
    response = requests.get(url, headers=myHeaders)
    bsInfo = bs(response.text, "html.parser")
    base_div = bsInfo.find("div", attrs={"class": "movie-brief-container"})
    li_info = base_div.find_all("li", attrs={"class": "ellipsis"})
    index = 0
    for base_li in li_info:
        if index == 0:
            for movie_type in base_li.find_all("a"):
                movie_types.append(movie_type.text)
        elif index == len(li_info)-1:
            movie_date = base_li.text
    movie["movie_types"] = movie_types
    movie["movie_date"] = movie_date


def save(movies=[]):
    pand = pandas.DataFrame(movies)
    pand.to_csv("./movie.csv", mode="a+", sep="\n", encoding="utf8")

getInfo(maoyanUrl)