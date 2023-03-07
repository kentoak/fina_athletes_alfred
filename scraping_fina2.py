# coding: utf-8
import requests
from bs4 import BeautifulSoup
import sys
import json
import re
import urllib.parse
import asyncio
from pyppeteer import launch

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
    for i in range(1, 100):
        await page.evaluate('window.scrollTo(0,'+ str(i * 1000) +')')
    await page.waitForSelector('.js-results-table-body')
    obj = []
    name=url.split("/")[-1].split("-")[0].capitalize()+" "+url.split("/")[-1].split("-")[1].capitalize()
    while True:
        try:
            show_more_button = await page.waitForSelector('.button.load-more-button.js-show-more-button')
            await show_more_button.click()
            k = await page.waitForSelector('.js-results-table-body')
            generated_element = await page.evaluate('(element) => element.innerHTML', k)
            content = await page.content()
            soup=BeautifulSoup(generated_element, "html.parser")
            for j in soup.select(".athlete-table__row"):
                #print(j)
                event,time,competition,poolLength,age,date,finapoint="","","","","","",""
                if j.select_one(".athlete-table__cell.athlete-table__cell--event"):
                    event=j.select_one(".athlete-table__cell.athlete-table__cell--event").get_text().strip()
                if j.select_one(".athlete-table__cell.athlete-table__cell--time.u-text-center"):
                    time_=j.select_one(".athlete-table__cell.athlete-table__cell--time.u-text-center").get_text().strip().split()
                    #print(" ".join(time_))
                    time=" =".join(time_)
                if j.select(".athlete-table__cell"):
                    # if len(j.select(".athlete-table__cell"))==8:
                    #     competition=j.select(".athlete-table__cell")[5].get_text().strip()
                    competition=j.select(".athlete-table__cell")[6].get_text().strip()
                if j.select_one(".athlete-table__cell.athlete-table__cell--points.u-text-center"):
                    finapoint=j.select_one(".athlete-table__cell.athlete-table__cell--points.u-text-center").get_text().strip()
                if j.select(".athlete-table__cell.u-text-center"):
                    if len(j.select(".athlete-table__cell.u-text-center"))==6:
                        #poolLength=j.select(".athlete-table__cell.u-text-center")[2].get_text().strip()
                        age=j.select(".athlete-table__cell.u-text-center")[3].get_text().strip()
                        date=j.select(".athlete-table__cell.u-text-center")[5].get_text().strip()
                #print(event,time)
                #print("age",age,"date",date)
                #print(competition)
                #print("finapoint is ...",finapoint)
                time=time.replace("==","=").lstrip('0')
                event=event.replace("Women","").replace("Men","")
                #print(name)
                tao = {
                    'title': event+" "+time,
                    'subtitle': name+":@"+competition+", age:"+age+", date:"+date,
                    'arg': event+" "+time+"\n"+name+" @"+competition+", age:"+age+", date:"+date
                }
                #print(tao)
                obj.append(tao)
        except:
            break
    await browser.close()
    jso = {'items': obj}
    sys.stdout.write(json.dumps(jso, ensure_ascii=False))

if __name__ == "__main__":
    #spell = " ".join(sys.argv[1:]).strip()
    spell = sys.argv[1:]
    asyncio.get_event_loop().run_until_complete(main(spell)) 