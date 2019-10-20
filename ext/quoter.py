#! python3
# coding: utf-8

import discord
import traceback
import asyncio
import time
import datetime
import re

from datetime import datetime
from discord.ext import commands
from .utils import checks, logger

class quoter:

    def __init__(self, bot):
        self.bot = bot
        self.testing = "612028415603638294"
        self.regex = r"https://discordapp\.com/channels/(\d{1,25})/(\d{1,25})/(\d{1,25})"
        
    async def on_message(self, message):
        try:
            if message.author.bot:
                return
            m=re.search(self.regex, message.content)
            if m:
                if m.group(1) == message.server.id:
                    await self.bot.delete_message(message)
                    # await self.bot.send_message(message.channel, "{}\n{}\n{}\n{}".format(m.group(0),m.group(1),m.group(2),m.group(3)))
                    getMessageChannel = self.bot.get_channel(m.group(2))
                    getMesssage = await self.bot.get_message(getMessageChannel,m.group(3))
                    embed_colour = 16777215 if str(getMesssage.author.top_role) == "@everyone" else getMesssage.author.color.value
                    emb = discord.Embed(description=getMesssage.content, color=embed_colour)
                    emb.set_author(name=getMesssage.author.name, icon_url=getMesssage.author.avatar_url, url="{}".format(m.group(0)))
                    if getMesssage.attachments:
                        file = getMesssage.attachments[0]['proxy_url']
                        fmt = getMesssage.attachments[0]['filename'].split(".")[1]
                        if file.lower().endswith(('png', 'jpeg', 'jpg', 'gif', 'webp')):
                            emb.set_image(url="{}".format(getMesssage.attachments[0]['proxy_url']))
                    emb.set_footer(text="Quoted from {}".format(getMesssage.timestamp.strftime("%I:%M:%S%p %d/%m/%Y")))
                    await self.bot.send_message(message.channel, embed=emb)
                else:
                    a=await self.bot.send_message(message.channel, "I'm only able to quote messages from this server.")
                    await asyncio.sleep(15)
                    await self.bot.delete_message(a)
        except Exception as e:
            await logger.errorLog("Quoter",None,e,traceback.format_exc())

    
def setup(bot):
    bot.add_cog(quoter(bot))
