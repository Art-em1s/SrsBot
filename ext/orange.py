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

from datetime import datetime
from discord.ext import commands
from .utils import checks, logger

class orange:

    def __init__(self, bot):
        self.bot = bot
        self.last = None
        self.thinking = "🤔"
        self.clap = "👏"
        self.artemis = "299556639294488576"
        self.orange = "186009740831227904"
        
    async def on_message(self, message):
        if message.channel.id == "609811763696762884":
            if message.author.id == self.orange:
                if "jon" in message.content.lower():
                    await self.bot.delete_message(message)
                # await self.bot.add_reaction(message, self.thinking)
    
def setup(bot):
    bot.add_cog(orange(bot))
