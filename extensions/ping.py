import hikari
import lightbulb
from datetime import datetime

ping_plugin = lightbulb.Plugin('Ping')

@ping_plugin.command
@lightbulb.command('ping', 'Get WolfBots current latency.')
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def ping(ctx: lightbulb.context.Context) -> None:
    await ctx.respond(
        embed=hikari.Embed(
            title='Ping',
            description=f'WolfBots current ping is: {ctx.app.heartbeat_latency*1000:.2f}ms',
            color=hikari.Color(0x007bf3),
            timestamp=datetime.now().astimezone()
        )
    )

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(ping_plugin)
