import hikari
import lightbulb
from datetime import datetime
import logging
import os
import sys

logging.getLogger()

restart_plugin = lightbulb.Plugin('Restart')

@restart_plugin.command
@lightbulb.command('restart', 'Restart WolfBot')
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def restart(ctx: lightbulb.context.Context) -> None:
    logging.info(f'User {ctx.author.username}:{ctx.author.id} has issued the restart command, restarting WolfBot.')
    await ctx.respond(
        embed=hikari.Embed(
            title='Restarting',
            description=f'Restarting WolfBot down.',
            color=hikari.Color(0x660000),
        )
    )
    os.execv(sys.executable, [sys.executable] + sys.argv)

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(restart_plugin)