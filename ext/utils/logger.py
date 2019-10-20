#! python3
# coding: utf-8

from ext.utils.webhook import DiscordWebhook, DiscordEmbed
import requests, json, discord,traceback
from datetime import datetime

async def errorLog(cmd = None,u :discord.Member = None,e :discord.errors = None,t = None):
    if not cmd:
        cmd = "N/a"
    if not e:
        e = "N/a"
    if not t:
        t = "N/a"
    try:
        webhook = DiscordWebhook(url="https://discordapp.com/api/webhooks/612036091289141278/AM6lsyt9xGkpFDrfzEDFOqI-1gvcGtxsFvoIusrNNluP0-VsSlH42bXD-EMM94vKmoOX")
        log = DiscordEmbed(color=0x00ff00)
        if u:
            log.add_field(name='User:', value='{}'.format(u), inline=True)
            log.add_field(name='User ID:', value='{}'.format(u.id), inline=True)
        log.add_field(name='Command:', value='`{}`'.format(cmd), inline=False)
        log.add_field(name='Error:', value='```py\n{}```'.format(e), inline=False)
        log.add_field(name='Description:', value='```py\n{}```'.format(t.replace("`", "")), inline=False)
        log.set_footer(text="Time: {}".format(datetime.now().strftime("%H:%M:%S %d-%m-%Y")))
        webhook.add_embed(log)
        webhook.execute()
    except Exception as e:
        print("Webhook Error Logger: {}".format(e))

async def say(t = None):
    if not t:
        t = "No content provided"
    try:
        if isinstance(t, str):
            t=t.replace("`", "")
        webhook = DiscordWebhook(url="https://discordapp.com/api/webhooks/612036407078289438/NHtD0w9GEHX9UeBQvawQQBCw0lq1SF84WwTLn_CA1vMXy4VJw-svGBZgVp-Pa8AtHwis")
        log = DiscordEmbed(color=0x00ff00)
        log.add_field(name='Webhook Message:', value='```{}```'.format(t), inline=False)
        log.set_footer(text="Time: {}".format(datetime.now().strftime("%H:%M:%S %d-%m-%Y")))
        webhook.add_embed(log)
        webhook.execute()
    except Exception as e:
        await errorLog("Log MSG",None,e,traceback.format_exc())
