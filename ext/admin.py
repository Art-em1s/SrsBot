#! python3
# coding: utf-8

import discord
import traceback
import random
from discord.ext import commands
from bot import initial_extensions as cogs
from .utils import checks, logger


class Admin:
    """Admin-only commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='rl', pass_context=True)
    async def _reload(self, ctx):
        """Reloads all extentions. - Art only"""
        try:
            await self.bot.delete_message(ctx.message)
            i=0
            msg=""
            for cog in cogs:
                try:
                    self.bot.unload_extension(cog)
                    self.bot.load_extension(cog)
                except Exception as e:
                    msg+="[x] {} - {}\n".format(cog[4:], e)
                else:
                    i+=1
            embed=discord.Embed(description="{}".format(msg), color=random.randint(0, 0xFFFFFF))
            embed.set_footer(text="{} cogs reloaded successfully.".format(i))
            await self.bot.say(embed=embed, delete_after=15)
        except Exception as e:
            await logger.errorLog(ctx.message.content,ctx.message.author,e,traceback.format_exc())
                
def setup(bot):
    bot.add_cog(Admin(bot))
