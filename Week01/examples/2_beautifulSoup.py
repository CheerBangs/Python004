import requests
from bs4 import BeautifulSoup as bs

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.3'

header = { 'user-agent': user_agent}

myurl = 'https://movie.douban.com/top250'

response = requests.get(myurl, headers=header)

bs_info = bs(response.text, 'html.parser')

# 查找某些标签
for tags in bs_info.find_all('div', attrs={'class': 'hd'}):
  for atag in tags.find_all('a',):
    # 打印电影链接
    print(atag.get('href'))
    # 打印电影名
    print(atag.find('span',).text)