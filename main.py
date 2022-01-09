#!/bin/python3
# WolfBot
# =======
# Personal bot of jjlr (https://github.com/jjlrjjlr).
#
# Copyright 2021-2022  jjlrjjlr (https://github.com/jjlrjjlr)

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published
#   by the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.

#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ------------

import hikari
import lightbulb
from os import name, path, makedirs
from sys import argv
from settings import Settings
import pin_db
import log_formatter
import logging
import control_daemon
import asyncio

logging.basicConfig(
    level=logging.DEBUG if '--debug' in argv else logging.INFO,
    handlers=[
        log_formatter.color_handler(),
        log_formatter.markdown_handler(dir_path='./logs')
    ]
)

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
    
    loop = asyncio.new_event_loop()
    loop.create_task(bot.start())
    loop.create_task(control_daemon.prompt(bot))
    loop.run_forever()


if __name__ == '__main__':
    if name != 'nt':
        import uvloop
        uvloop.install()
    main()