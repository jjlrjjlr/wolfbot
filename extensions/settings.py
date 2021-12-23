import lightbulb
import hikari

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
    ctx.bot.d.settings.set_save_channel(ctx.get_guild().id.real, ctx.options.channel.strip('<>#'))

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(settings_plugin)