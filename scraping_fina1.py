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
    url = spell[0]
    #url =  "http://swim.seiko.co.jp/"
    browser = await launch()
    #browser = await launch(headless=False) #ブラウザを表示する
    page = await browser.newPage()
    # ページ遷移して読み込みが終わるまで待つ
    await asyncio.wait([
        page.goto(url),
        page.waitForNavigation(),
    ])
    await page.waitForSelector('.body-content')
    target = await page.J(".body-content")
    generated_element = await page.evaluate('(element) => element.innerHTML', target)
    soup=BeautifulSoup(generated_element, "html.parser")
    obj = []
    name=url.split("/")[-1].split("-")[0].capitalize()+" "+url.split("/")[-1].split("-")[1].capitalize()
    if soup.select_one("tbody"):
        for j in soup.select("tr"):
            # if j.select("td"):
            #     for k in j.select("td"):
            #         if "-"==k.get_text().strip():
            #             break
            #         print(k.get_text().strip())
            event,time,competition,poolLength,age,date="","","","","",""
            if j.select_one(".athlete-table__cell.athlete-table__cell--event"):
                event=j.select_one(".athlete-table__cell.athlete-table__cell--event").get_text().strip()
            if j.select_one(".athlete-table__cell.athlete-table__cell--time.u-text-center"):
                time_=j.select_one(".athlete-table__cell.athlete-table__cell--time.u-text-center").get_text().strip().split()
                #print(" ".join(time_))
                time=" =".join(time_)
            if j.select(".athlete-table__cell"):
                if len(j.select(".athlete-table__cell"))==8:
                    competition=j.select(".athlete-table__cell")[5].get_text().strip()
            if j.select(".athlete-table__cell.u-text-center"):
                if len(j.select(".athlete-table__cell.u-text-center"))==6:
                    poolLength=j.select(".athlete-table__cell.u-text-center")[2].get_text().strip()
                    age=j.select(".athlete-table__cell.u-text-center")[3].get_text().strip()
                    date=j.select(".athlete-table__cell.u-text-center")[5].get_text().strip()
            #print("poolLength",poolLength,"age",age,"date",date)
            #print(competition)
            if not poolLength:
                continue
            pooldict={"25m":"SCM","50m":"LCM"}
            # tao = {
            #         'title': name+"    "+pooldict[poolLength]+" "+event.replace("Women","").replace("Men","")+" "+time,
            #         'subtitle': "@"+competition+", age:"+age+", date:"+date,
            #         'arg': ""
            #     }
            tao = {
                    'title': pooldict[poolLength]+" "+event.replace("Women","").replace("Men","")+" "+time,
                    'subtitle': name+" @"+competition+", age:"+age+", date:"+date,
                    'arg': pooldict[poolLength]+" "+event.replace("Women","").replace("Men","")+" "+time+"\n"+name+" @"+competition+", age:"+age+", date:"+date
                }
            obj.append(tao)
    await browser.close()
    jso = {'items': obj}
    sys.stdout.write(json.dumps(jso, ensure_ascii=False))

if __name__ == "__main__":
    #spell = " ".join(sys.argv[1:]).strip()
    spell = sys.argv[1:]
    asyncio.get_event_loop().run_until_complete(main(spell)) 




    