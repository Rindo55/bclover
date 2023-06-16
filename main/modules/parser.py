import asyncio
from main.modules.schedule import update_schedule
from main.modules.usschedule import update_schedulex
from main.modules.utils import status_text
from main import status
from main.modules.db import get_animesdb, get_uploads, save_animedb
import feedparser
from main import queue
from main.inline import button1

def trim_title(title: str):
    title = title.replace("Demon Slayer S04E04 1080p WEB H.264 E-AC-3 -Yandere-Raws (AMZN) (Kimetsu no Yaiba: Katanakaji no Sato-hen)", "Demon Slayer Kimetsu No Yaiba To the Swordsmith Village - 04")
    title = title.replace("Black Clover Sword of the Wizard King 2023 1080p NF WEB-DL DDP5.1 H 264-VARYG (Black Clover: Mahou Tei no Ken, Dual-audio, Multi-Subs)", "Black Clover Sword of the Wizard King")
    ext = ".mkv"
    title = title + ext
    return title

def parse():
    a = feedparser.parse("https://nyaa.si/?page=rss&u=varyg1001")
    b = a["entries"]
    b = b[0:1]
    data = []    

    for i in b:
        item = {}
        item['title'] = trim_title(i['title'])
        item['size'] = i['nyaa_size']   
        item['link'] = "magnet:?xt=urn:btih:" + i['nyaa_infohash']
        data.append(item)
    data.reverse()
    return data

async def auto_parser():
    while True:
        try:
            await status.edit(await status_text("Parsing Rss, Fetching Magnet Links..."),reply_markup=button1)
        except:
            pass

        rss = parse()
        data = await get_animesdb()
        uploaded = await get_uploads()

        saved_anime = []
        for i in data:
            saved_anime.append(i["name"])

        uanimes = []
        for i in uploaded:
            uanimes.append(i["name"])

        for i in rss:
            if i["title"] not in uanimes and i["title"] not in saved_anime:
                if ".mkv" in i["title"] or ".mp4" in i["title"]:
                    title = i["title"]
                    await save_animedb(title,i)

        data = await get_animesdb()
        for i in data:
            if i["data"] not in queue:
                queue.append(i["data"])    
                print("Saved ", i["name"])   

        try:
            await status.edit(await status_text("Idle..."),reply_markup=button1)
            await asyncio.sleep(6)
        except:
            pass

        await asyncio.sleep(45)
