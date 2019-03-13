#! python3
# coding: utf-8

import logging
import asyncio
import sys
import discord
import random
from discord.ext import commands

# logging
logging.basicConfig(level=logging.INFO, filename='bot.log', format='[%(levelname)s] | [%(asctime)s] | [%(name)s] | %(message)s') # include timestamp

# bot declaration
prefix = "+"

description = '''Hello! I'm SrsBot.
Here's a list of stuff I can do:'''
bot = commands.Bot(command_prefix=prefix, description=description, no_pm=True, pm_help=True)

# Cogs addition
initial_extensions = [
    'ext.admin',
    'ext.usercmds'
]

# Error handling
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        await bot.send_message(ctx.message.author, 'This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await bot.send_message(ctx.message.channel, 'This command is disabled and cannot be used.')
    elif isinstance(error, commands.CommandInvokeError):
        pass  # do nothing
    elif isinstance(error, commands.CheckFailure):
        await bot.send_message(ctx.message.channel, "You don't have permission to do this.")
    elif isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.CommandOnCooldown):
        await bot.delete_message(ctx.message)
        sent = await bot.send_message(ctx.message.channel, "This command is on cooldown. Try again in {}s.".format(int(error.retry_after)))
        await asyncio.sleep(5)
        await bot.delete_message(sent)

@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name="+help"), afk=False)


if __name__ == '__main__':
    if any('debug' in arg.lower() for arg in sys.argv):
        bot.command_prefix = '^'
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    bot.run(sys.arg[1])
