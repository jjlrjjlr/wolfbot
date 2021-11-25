#!/bin/python3
# WolfBot
# ------------

import hikari
import lightbulb
from os import name as os_name

def main():
    with open('.secret/token', 'r') as token_file:
        __token = token_file.read().strip()
    with open('.secret/guild', 'r') as guild_file:
        __guild = int(guild_file.read().strip())

    bot = lightbulb.BotApp(
        token=__token,
        intents=hikari.Intents.ALL,
        ignore_bots=True,
        default_enabled_guilds=__guild
    )

    bot.load_extensions_from('./extensions/')
    bot.run()

if __name__ == '__main__':
    if os_name != 'nt':
        import uvloop
        uvloop.install()
    main()