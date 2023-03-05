# coding: utf-8
import requests
from bs4 import BeautifulSoup
import sys
import json
import re
import urllib.parse
import asyncio
from pyppeteer import launch
#from requests_html import HTML

async def main(spell):
    url = "https://www.fina.org/athletes/?gender=&discipline=&nationality=&name=" + spell
    browser = await launch()
    #browser = await launch(headless=False) #ブラウザを表示する
    page = await browser.newPage()
    # ページ遷移して読み込みが終わるまで待つ
    await asyncio.wait([
        page.goto(url),
        page.waitForNavigation(),
    ])
    # # contentを取得し、request-htmlのparserで読み込み
    # content = await page.content()
    # html = HTML(html=content)
    # # 取得したいデータのparse
    # target = html.find('.js-athletes-container', first=True).text
    # print(target)
    
    #pyppeteer
    #target = await page.J('.js-athletes-table-body')
    await page.waitForSelector('.js-athletes-table-body')
    target = await page.J('.js-athletes-table-body')
    #title = await page.evaluate('(target) => target.textContent',target)
    generated_element = await page.evaluate('(element) => element.innerHTML', target)
    #print(type(generated_element))
    soup=BeautifulSoup(generated_element, "html.parser")
    #print(soup)
    #print(type(soup))
    obj = []
    if soup.select("tr"):
        for j in soup.select("tr"):
            # if j.select("td"):
            #     for k in j.select("td"):
            #         if "-"==k.get_text().strip():
            #             break
            #         print(k.get_text().strip())
            name,country,discipline,gender,birth="","","","",""
            if j.select_one(".athlete-table__name"):
                name=j.select_one(".athlete-table__name").get_text().strip()
            if j.select_one(".athlete-table__country"):
                country=j.select_one(".athlete-table__country").get_text().strip()
            if j.select_one(".athlete-table__discipline"):
                discipline=j.select_one(".athlete-table__discipline").get_text().strip()
            if j.select(".athlete-table__cell.u-hide-tablet.u-text-center"):
                if len(j.select(".athlete-table__cell.u-hide-tablet.u-text-center"))==2:
                    gender=j.select(".athlete-table__cell.u-hide-tablet.u-text-center")[0].get_text().strip()
                    birth=j.select(".athlete-table__cell.u-hide-tablet.u-text-center")[1].get_text().strip()
            link=""
            if j.select_one(".athlete-table__cta-link"):
                if "href" in j.select_one(".athlete-table__cta-link").attrs:
                    link="https:"+j.select_one(".athlete-table__cta-link")["href"]
            #print(link)
            #print(name,country,discipline,gender,birth)
            if discipline=="Swimming":
                tao = {
                        'title': name+" ("+country+")",
                        'subtitle': gender+" "+birth,
                        'arg': link
                    }
                obj.append(tao)
    await browser.close()
    jso = {'items': obj}
    sys.stdout.write(json.dumps(jso, ensure_ascii=False))

if __name__ == "__main__":
    spell = " ".join(sys.argv[1:]).strip()
    asyncio.get_event_loop().run_until_complete(main(spell)) 

def main(spell):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
    }
    url = "https://www.fina.org/athletes/?gender=&discipline=&nationality=&name=" + spell
    #print(url)
    source = requests.get(url, headers=headers)
    soup = BeautifulSoup(source.content, "html.parser")
    if soup.select_one(".js-athletes-container"):
        print(soup.select_one(".js-athletes-container"))
        if soup.select_one(".js-athletes-container").select("td"):
            for j in soup.select_one(".js-athletes-container").select("td"):
                print(j)
    return


def onlyAlphabet(text):
    re_roman = re.compile(r'^[a-zA-Z\.]+$')  # a-z:小文字、A-Z:大文字
    return re_roman.fullmatch(text)

def onlyJa(text):
    re_ja = re.compile(
        r'^[\u4E00-\u9FFF|\u3040-\u309F|\u30A0-\u30FF]{1,10}[\u4E00-\u9FFF|\u3040-\u309F|\u30A0-\u30FF]{1,10}$')
    return re_ja.fullmatch(text)

def contains_doubleByte_char(text):
    # 正規表現を使用して、文章の中に全角文字が含まれているかどうかを判定する
    if re.search(r'’| / ', text):
        return False
    return bool(re.search(r'[^\x00-\x7F]', text))

# if __name__ == '__main__':
#     spell = " ".join(sys.argv[1:]).strip()
#     print(spell)
#     main(spell)
    #print("\nout1 is        \n",out1)
    