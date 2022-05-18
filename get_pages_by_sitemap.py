from bs4 import BeautifulSoup
import urllib.request as req
import os.path
import re

def parse_sitemap(url):
    savename = "delete-ok.text"
    if os.path.exists(savename):
        os.remove(savename)
    req.urlretrieve(url, savename)

    xml = open(savename, "r", encoding="utf-8").read()
    soup = BeautifulSoup(xml, 'html.parser')

    pages = [] 
    #ページリストを取得
    for i in soup.find_all("url"):
        loc = i.find('loc').string.strip()
        pages.append(loc)

    #sitemap.xmlが入れ子の場合は再帰的に呼び出す
    for i in soup.find_all("sitemap"):
        loc = i.find('loc').string.strip()
        pages.extend(parse_sitemap(loc))

    #後処理
    if os.path.exists(savename):
        os.remove(savename)

    return pages

if __name__ == '__main__':
    #sitemap.xmlを取得する
    url = "https://shigoto-web.co.jp/tensyoku/sitemap.xml"
    pages = parse_sitemap(url)

    print("--------------")
    for loc in pages:
        print(loc)
    print("--------------")
