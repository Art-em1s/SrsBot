#! python3
# coding: utf-8

import discord
from .utils import checks, logger
from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands
from PyDictionary import PyDictionary
import json
import asyncio



class UserCommands:

    def __init__(self, bot):
        self.bot = bot
      
    @checks.is_owner()
    @commands.command(hidden=True, name='rb', aliases=['RB', 'Rb', 'rB'], pass_context=True)
    async def _shut_down(self, ctx):
        """Reboots the bot"""
        try:
            await self.bot.delete_message(ctx.message)
            await self.bot.close()
        except Exception as e:
            await logger.errorLog(message.content,message.author,e,traceback.format_exc())     
            
    @checks.is_owner()
    @commands.command(hidden=True, pass_context=True)
    async def type(self, ctx):
        """Reboots the bot"""
        try:
            while True:
                await self.bot.send_typing(ctx.message.channel)
                await asyncio.sleep(9)
        except Exception as e:
            await logger.errorLog(message.content,message.author,e,traceback.format_exc())
            
    @commands.command(pass_context=True, aliases=['color', 'Colour', 'Color'])
    async def colour(self, ctx, hex):
        try:
            author = ctx.message.author.id
            server = ctx.message.server
            message = ctx.message
            await self.bot.delete_message(message)
            if not hex:
                await self.bot.say("You need to include a colour code, ie #00ff00", delete_after=15)
                return
            if "#" in hex:
                hex = hex.replace("#", "")
            hex = int(hex, 16)
            role = discord.utils.get(server.roles, name=message.author.id)
            if not role:
                role = await self.bot.create_role(ctx.message.server)
                await self.bot.edit_role(ctx.message.server, role, name=message.author.id, color=discord.Colour(value=hex))
                await self.bot.add_roles(ctx.message.author, role)
            else:
                await self.bot.edit_role(server, role, color=discord.Colour(value=hex))
            await self.bot.say("Your colour has been updated.", delete_after=15)
        except Exception as e:
            await logger.errorLog(message.content,message.author,e,traceback.format_exc())
            
    @commands.command(pass_context=True)
    async def g(self, ctx, *terms: str):
        """Generate a Google search."""
        await self.bot.delete_message(ctx.message)
        await self.bot.say('https://www.google.com/search?q=' + '+'.join(terms), delete_after=30)
        
    @commands.command(pass_context=True)
    async def define(self, ctx, term):
        """Returns the definition of a word.
        """
        try:
            await self.bot.delete_message(ctx.message)
            # if ctx.message.author.id != "299556639294488576":
                # await self.bot.say("Command down for maintenance", delete_after=15)
                # return
            dictionary=PyDictionary()
            msg_out = "```Definition for: {}\n\n".format(term.title())
            json_data = dictionary.meaning(term)
            data = json.dumps(json_data)
            await logger.say(data)
            if "Noun" in data:
                msg_out+="Noun:\n"
                i=0
                for item in json_data['Noun']:
                    i+=1
                    if i>3:
                        break
                    msg_out+="{}) {}\n".format(i,item.replace("(", "").capitalize())
                msg_out+="\n"
            if "Verb" in data:
                msg_out+="Verb:\n"
                i=0
                for item in json_data['Verb']:
                    i+=1
                    if i>3:
                        break
                    msg_out+="{}) {}\n".format(i,item.replace("(", "").capitalize())
                msg_out+="\n"
            if "Adjective" in data:
                msg_out+="Adjective:\n"
                i=0
                for item in json_data['Adjective']:  
                    i+=1
                    if i>3:
                        break
                    msg_out+="{}) {}\n".format(i,item.replace("(", "").capitalize())
                msg_out+="\n"
            msg_out+="```"
            if msg_out != "``````":
                await self.bot.say(msg_out, delete_after=60)
            else:
                await self.bot.say("Nothing found, check your spelling or ensure you're only checking a single word.", delete_after=15)
        except Exception as e:
            await logger.errorLog(message.content,message.author,e,traceback.format_exc())
            
        
def setup(bot):
    bot.add_cog(UserCommands(bot))
