import lightbulb
import hikari

celsius_plugin = lightbulb.Plugin('Celsius')

@celsius_plugin.command
@lightbulb.option('fahrenheit', 'Temperature in Fahrenheit to convert.', required=True, type=float)
@lightbulb.command('celsius', 'Convert Fahrenheit to Celsius.')
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def celsius_command(ctx: lightbulb.context.Context) -> None:
    await ctx.respond(
        embed=hikari.Embed(
            title='Fahrenheit to Celsius',
            description=f'({ctx.options.fahrenheit} - 32) * (5/9) = **{((int(ctx.options.fahrenheit) - 32) * (5/9)):.1f}**',
            color=hikari.Color(0x66FF00)
        )
    )

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(celsius_plugin)