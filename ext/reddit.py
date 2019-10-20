#! python3
# coding: utf-8

import discord
import traceback
import random
import asyncio
import sqlite3
import time
import requests
import json
import praw
import lxml
import re
import os

from datetime import datetime
from discord.ext import commands
from .utils import checks, logger

class reddit:
    """Hourly Reddit posts."""

    def __init__(self, bot):
        self.bot = bot
        self.last = None
        self.database = "/home/bot/SrsBot/db/srs.db"
        self.channels = ["610269630564663353", "609813694708449281", "609814158749466654","609823719308656700", "609815572535967744", "609814764830588938"]
        
        #(channel_id, subreddit, category)
        self.urls = [
        ("610269630564663353", "FoodPorn"),
        ("610269630564663353", "BreakfastFood"),
        ("610269630564663353", "food"),
        ("610269630564663353", "JapaneseFood"),
        ("610269630564663353", "KoreanFood"),
        ("610269630564663353", "GifRecipes"),
        ("610269630564663353", "interestingasfuck"),
        ("610269630564663353", "mechanical_gifs"),
        ("610269630564663353", "gardening"),
        ("610269630564663353", "woodworking"),
        ("610269630564663353", "Canning"),
        ("610269630564663353", "DIY"),
        ("610269630564663353", "Art"),
        ("609813694708449281", "aww"),
        ("609813694708449281", "NatureIsFuckingLit"),
        ("609813694708449281", "Eyebleach"),
        ("609813694708449281", "Panda_Gifs"),
        ("609813694708449281", "redpanda_gifs"),
        ("609813694708449281", "redpandas"),
        ("609813694708449281", "natureismetal"),
        ("609813694708449281", "AnimalsBeingDerps"),
        ("609813694708449281", "EarthPorn"),
        ("609814158749466654", "science"),
        ("609814764830588938", "todayilearned"),
        ("609814764830588938", "NoStupidQuestions"),
        ("609814764830588938", "DoesAnybodyElse"),
        ("609814764830588938", "explainlikeimfive"),
        ("609814764830588938", "WDP"),
        ("609814764830588938", "TooAfraidToAsk"),
        ("609814764830588938", "HumansBeingBros"),
        ("609814764830588938", "AskReddit"),
        ("609814158749466654", "askscience"),
        ("609814158749466654", "science"),
        ("609814158749466654", "Futurology"),
        ("609814158749466654", "space"),
        ("609814158749466654", "MostBeautiful"),
        ("609814158749466654", "spaceporn"),
        ("609814158749466654", "Astronomy"),
        ("609814158749466654", "auroraporn"),
        ("609814158749466654", "Cosmos"),
        ("609814158749466654", "rocketlaunches"),
        ("609814158749466654", "Spaceexploration"),
        ("609823719308656700", "business"),
        ("609823719308656700", "digitalnomad"),
        ("609823719308656700", "Entrepreneur"),
        ("609815572535967744", "listentothis"),
        ("609815572535967744", "videos"),
        ("609815572535967744", "Games"),
        ("609815572535967744", "books"),
        ("609815572535967744", "Music"),
        ("609815572535967744", "television"),
        ("609815572535967744", "comics")
        ] 
        
        self.testing = "612028415603638294"
        self.reddit = "https://redd.it/"
        self.filter = ["gyazo", "redd.it", "youtube.com"]
        
    async def on_ready(self):
        try:
            await self.do_reddit_loop()
        except Exception as e:
            await logger.errorLog("reddit on_ready",None,e,traceback.format_exc())
            
    async def on_resume(self):
        try:
            await self.do_reddit_loop()
        except Exception as e:
            await logger.errorLog("reddit on_resume",None,e,traceback.format_exc())
            
    async def do_reddit_loop(self):
        try:
            while True:
                db = sqlite3.connect(self.database)
                cursor  = db.cursor()
                x=cursor.execute("select * from lastcheck").fetchone()
                db.commit()
                cursor.close()
                db.close()
                self.last = int(x[0])
                # self.last = 0
                if self.last is None: #if connection to db fails for some reason
                    await logger.say("None triggered iter_urls")
                    await self.iter_urls()
                elif self.last <= int(time.time())-10800:
                    await logger.say("triggered iter_urls")
                    await self.iter_urls()
                else:
                    await asyncio.sleep(60*10)
        except Exception as e:
            await logger.errorLog("Do_reddit_loop",None,e,traceback.format_exc())
            
                
    async def iter_urls(self):
        try:    
            await self.update_db()
            id = "000"
            secret = "111"
            reddit = praw.Reddit(client_id=id, client_secret=secret, user_agent='SrsBot')
            for channel in self.channels:
                urls = [item for item in self.urls if item[0] == channel]
                url = random.choice(urls)
                await logger.say("URLS: {} | URL: {}".format(urls, url))
                await asyncio.sleep(1)
                channel_id = url[0]
                subreddit_name = url[1]
                
                ch = self.bot.get_channel(channel_id)
                # ch = self.bot.get_channel(self.testing)
                subreddit = reddit.subreddit(subreddit_name)
                for post in subreddit.top(time_filter='week'):
                    # print(vars(post))
                    if post.distinguished is None and post.stickied is False:
                        check = await self.check_posted(post.id)
                        if not check and self.last <= int(time.time())-10800:
                            img = await self.fetch_meta(post.url)
                            # x=True
                            x = await self.post_emb(ch, post.title, post.id, img)
                            if x is True:
                                break
                else:
                    await logger.say("No posts for {}".format(subreddit_name))
                    break
                continue
        except Exception as e:
            await logger.errorLog("iter_urls",None,e,traceback.format_exc())
            return
            
    async def check_posted(self, post_id):
        db = sqlite3.connect(self.database)
        cursor  = db.cursor()
        check=cursor.execute("select * from reddit where id = ?",(post_id,)).fetchone()
        cursor.close()
        db.close()
        return post_id if check else None
        
    async def post_emb(self, ch, title, post_id, image):
        try:
            if not title or not post_id:
                if not title:
                    await logger.say("skipping due to missing title")
                elif not post_id:
                    await logger.say("skipping due to missing post id")
                return False
            else:
                embed=discord.Embed(title="{}{}".format(title[:250], "..." if len(title)>249 else ""), url="{}".format("https://redd.it/{}".format(post_id)), color=random.randint(0, 0xFFFFFF))
                if image is not None:
                    embed.set_image(url=image)  
                await self.bot.send_message(ch, embed=embed)
                await self.mark_posted(post_id)
                return True
        except Exception as e:
            await logger.errorLog("post_emb",None,e,traceback.format_exc())
            await logger.say("{} | {} | {}".format(title, post_id, image))
            return False
            
    async def mark_posted(self, post_id):
        # return 
        db = sqlite3.connect(self.database)
        cursor  = db.cursor()
        cursor.execute("insert into reddit (id) values (?)",(post_id,))
        db.commit()
        cursor.close()
        db.close()
        
    async def update_db(self):
        try:
            t=int(time.time())
            db = sqlite3.connect(self.database)
            cursor  = db.cursor()
            cursor.execute("update lastcheck set time = ?", (t,))
            db.commit()
            cursor.close()
            db.close()
            await logger.say("lastcheck updated - {}".format(t))
            return
        except Exception as e:
            await logger.errorLog("update lastcheck",None,e,traceback.format_exc())
        
    async def fetch_meta(self, url):
        regex = r"property=\"og:image\"\s(name=\"og:image\" )?content=\"(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_\+.~#?&//=]*)\""
        no_image = "https://w1z0.xyz/i/bg9lCZS3pf.png"
        reddit_no_image = "https://www.redditstatic.com/new-icon.png"
        images_check = ('png', 'jpeg', 'jpg', 'gif', 'webp')
        if url.endswith(images_check):
            await logger.say("image save triggered for {}".format(url))
            img = await self.save_image(url)
            return img
        elif ("https://v.redd.it" or "https://redd.it") in url:
            return reddit_no_image
        elif "youtube.com" in url:
            return "https://img.youtube.com/vi/{}/0.jpg".format(url.split("=")[1])
        else:
            html = requests.get(url).text
            match = re.search(regex, html, re.IGNORECASE)
            if match is None:
                return None
            elif match.group(2):
                return match.group(2)
            else:
                await logger.say("meta none for {}".format(post.url))
                return None
                
    async def save_image(self, url):
        if url.lower().endswith(('png', 'jpeg', 'jpg', 'gif', 'webp')):
            fmt = url[-4:]
            file_name="{}.{}".format(int(time.time()),fmt)
            fp="/var/www/html/w1z0.xyz/i/{}".format(file_name)#file path
            if os.path.isfile(fp) is False:
                try:
                    img_data = requests.get(url).content #download image
                    with open(fp, 'wb') as handler: #save
                        handler.write(img_data)
                except Exception as e:
                    await logger.errorLog("File Saver",None,e,traceback.format_exc())
            return "https://w1z0.xyz/i/{}".format(file_name)
    
def setup(bot):
    bot.add_cog(reddit(bot))
