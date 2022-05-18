import get_pages_by_sitemap
from bs4 import BeautifulSoup
from urllib import request
import os.path
import re
import time
import pprint
import pandas as pd

def get_tdkh1(url):
    tdkh1 = {}
    html = request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup.prettify())

    #url
    tdkh1['url'] = url

    #title
    t = soup.find("title")
    if t is None:
        t = ""
    else:
        t = t.text.strip()
    tdkh1['title'] = t

    #meta_descriptnion
    d = soup.find("meta", {"name":"description"})
    if d is None:
        d = ""
    else:
        d = d["content"].strip()
    tdkh1['description'] = d

    #meta_keywords
    k = soup.find("meta", {"name":"keywords"})
    if k is None:
        k = ""
    else:
        k = k["content"].strip()
    tdkh1['keywords'] = k

    #h1
    h1 = soup.find("h1")
    if h1 is None:
        h1_text = ""
    else:
        h1_text = h1.text.strip()
        for img in h1.find_all("img"):
            h1_text = h1_text + "<img>" + img["alt"]
    tdkh1['h1'] = h1_text

    return tdkh1

def get_tdkh1s(urls):
    tdkh1s = []
    for url in urls:
        tdkh1s = tdkh1s + [get_tdkh1(url)]
        time.sleep(0.5)

    #Excelに保存
    col_names = ['url', 'title', 'meta_description', 'meta_keywords', 'h1']
    lines = []
    
    for tdkh1 in tdkh1s:
        lines.append([tdkh1["url"], tdkh1["title"], tdkh1["description"], tdkh1["keywords"], tdkh1["h1"]])

    df = pd.DataFrame(lines, columns=col_names)

    with pd.ExcelWriter('./tdkh1s.xlsx') as writer:
        df.to_excel(writer, sheet_name='TDKh1一覧')

    return tdkh1s

if __name__ == '__main__':
    url = "https://shigoto-web.co.jp/tensyoku/sitemap.xml"
    urls= get_pages_by_sitemap.parse_sitemap(url)
    tdkh1s = get_tdkh1s(urls)

    print("--------------")
    print("完了")
    print("--------------")
