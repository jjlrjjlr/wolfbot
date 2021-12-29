import hikari
import lightbulb
from datetime import datetime
import logging

logging.getLogger()

shutdown_plugin = lightbulb.Plugin('Shutdown')

@shutdown_plugin.command
@lightbulb.command('shutdown', 'Shutdown WolfBot')
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def shutdown(ctx: lightbulb.context.Context) -> None:
    logging.info(f'User {ctx.author.username}:{ctx.author.id} has issued the shutdown command, terminating WolfBot.')
    await ctx.respond(
        embed=hikari.Embed(
            title='Shutting Down',
            description=f'Shutting WolfBot down.',
            color=hikari.Color(0x660000),
        )
    )
    await ctx.bot.close()

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(shutdown_plugin)
