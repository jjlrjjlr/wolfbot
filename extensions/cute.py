import lightbulb
import hikari
from datetime import datetime

cute_plugin = lightbulb.Plugin('Cute')

@cute_plugin.command
@lightbulb.command('cute', 'Let the very best boyfriend know how cute he is.')
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def cute_command(ctx: lightbulb.context.Context) -> None:
    await ctx.respond(
        embed=hikari.Embed(
            title='Ranger is cute',
            description=f'Ranger is the absolute cutest, most adorable, best boyfriend ever. <3',
            color=hikari.Color(0x007bf3),
            timestamp=datetime.now().astimezone()
        )
    )

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(cute_plugin)
