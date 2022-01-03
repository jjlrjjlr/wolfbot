import lightbulb
import hikari
import logging
from datetime import datetime
import time

logging.getLogger()

settings_plugin = lightbulb.Plugin('Settings')

@settings_plugin.command
@lightbulb.command('settings', 'Edit bot settings.')
@lightbulb.implements(lightbulb.commands.SlashCommandGroup)
async def settings_main(ctx: lightbulb.context.Context) -> None:
    pass

@settings_main.child
@lightbulb.option('channel', 'Channel id.', required=True)
@lightbulb.command('saved_message_channel', 'Channel to save messages to from the /save command.')
@lightbulb.implements(lightbulb.commands.SlashSubCommand)
async def saved_message_channel(ctx: lightbulb.context.Context) -> None:
    try:
        ctx.bot.d.settings.set_save_channel(ctx.get_guild().id.real, ctx.options.channel.strip('<>#'))
        logging.info(f'Guild {ctx.get_guild().name}:{ctx.get_guild().id} have updated save channel to {ctx.options.channel.strip("<>#")}')
        await ctx.respond(
            hikari.Embed(
                title='Setting Updated',
                description=f'Save channel has been successfully updated to <#{ctx.options.channel.strip("<>#")}>\n'\
                f'<t:{int(time.mktime(datetime.now().timetuple()))}>',
                color=hikari.Color(0x66FF00)
            )
        )
    except Exception as e:
        logging.traceback()

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(settings_plugin)