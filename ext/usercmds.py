#! python3
# coding: utf-8

import discord
from .utils import checks
from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands



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
            print("{}\n{}\n{}\n{}".format(message.content,message.author,e,traceback.format_exc()))
            
    @commands.command(pass_context=True, aliases=['color'])
    async def colour(self, ctx, hex):
        try:
            author = ctx.message.author.id
            server = ctx.message.server
            message = ctx.message
            await self.bot.delete_message(message)
            if not hex:
                await self.bot.say("You need to include a colour code, ie #00ff00", delete_after=15)
            if "#" in hex:
                hex = hex.replace("#", "")
            hex = int(hex, 16)
            role = discord.utils.get(server.roles, name=message.author.id)
            if not role:
                role = await self.bot.create_role(ctx.message.server)
                await self.bot.edit_role(ctx.message.server, role, name=message.author.id, color=discord.Colour(value=hex))
                await self.bot.add_roles(ctx.message.author, role)
            else:
                await self.bot.edit_role(server, majin, color=discord.Colour(value=hex))
            await self.bot.say("Your colour has been updated.", delete_after=15)
        except Exception as e:
            print("{}\n{}\n{}\n{}".format(message.content,message.author,e,traceback.format_exc()))
            
    @commands.command(pass_context=True)
    async def g(self, ctx, *terms: str):
        """Generate a Google search."""
        await self.bot.delete_message(ctx.message)
        await self.bot.say('https://www.google.com/search?q=' + '+'.join(terms), delete_after=30)
            
            
    @commands.command(pass_context=True)
    async def topic(self, ctx):
        await self.bot.delete_message(ctx.message)
        await self.bot.say("Current Channel Topic: {}".format(ctx.message.channel.topic if ctx.message.channel.topic else "None Set."), delete_after=120)
        
def setup(bot):
    bot.add_cog(UserCommands(bot))
