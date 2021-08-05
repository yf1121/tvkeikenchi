import requests
from bs4 import BeautifulSoup
import re

def get(pf, area):
    pf = str(pf)
    area = str(area)
    url = "https://www.tvkingdom.jp/rss/schedulesByCurrentTime.action?group=" + pf + "&stationAreaId=" + area
    headers_dic = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
    res = requests.get(url, headers=headers_dic)
    # BeautifulSoupで解析
    soup = BeautifulSoup(res.text, 'html.parser')

    # スクレイピング
    data = []
    for rss in soup.findAll('item'):
        ch = re.findall(r'\(Ch\.([0-9]+)\)', rss.description.string)
        dic = {'ch': ch[0], 'title': rss.title.string, 'link': rss.get('rdf:about'), 'description': rss.description.string}
        data.append(dic)
    
    return data

def detail(url):
    headers_dic = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
    res = requests.get(url, headers=headers_dic)
    # BeautifulSoupで解析
    soup = BeautifulSoup(res.text, 'html.parser')

    # title タグの文字列を取得する
    dd = soup.find_all('dd')
    pginfo = re.split('[\s\(\)（）]+', dd[2].get_text().strip())

    # スクレイピング
    src = ['', '', '', '', '', '', '', '']
    src[0] = soup.find('h1', class_='basicContTitle').get_text()
    src[1] = soup.find('h3', class_='blTitleSub basicTit', text='番組概要').next_sibling.next_sibling.get_text().strip()
    src[2] = soup.find('h3', class_='blTitleSub basicTit', text='番組詳細').next_sibling.next_sibling.get_text().strip()
    src[3] = dd[4].get_text().split(' , ')
    src[4] = pginfo[0]
    src[5] = pginfo[2]
    src[6] = pginfo[4]
    src[7] = dd[3].get_text()

    return src
