#!/bin/python3
# WolfBot
# ------------

import hikari
import lightbulb
from os import name, path, makedirs
from settings import Settings
import pin_db

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

    bot.d.settings = Settings()

    if not path.exists(bot.d.settings.get_save_database_file()):
        makedirs(path.dirname(bot.d.settings.get_save_database_file()), exist_ok=True)
        pin_db.create_database(bot)

    bot.load_extensions_from('./extensions/')
    bot.run()

if __name__ == '__main__':
    if name != 'nt':
        import uvloop
        uvloop.install()
    main()