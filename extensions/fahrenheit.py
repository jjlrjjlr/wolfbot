import lightbulb
import hikari

fahrenheit_plugin = lightbulb.Plugin('Celsius')

@fahrenheit_plugin.command
@lightbulb.option('celsius', 'Temperature in Celsius to convert.', required=True, type=float)
@lightbulb.command('fahrenheit', 'Convert Celsius to Fahrenheit.')
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def fahrenheit_command(ctx: lightbulb.context.Context) -> None:
    await ctx.respond(
        embed=hikari.Embed(
            title='Celsius to Fahrenheit',
            description=f'{ctx.options.celsius} * (9/5) + 32 = **{(int(ctx.options.celsius) * (9/5) + 32):.1f}**',
            color=hikari.Color(0x66FF00)
        )
    )

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(fahrenheit_plugin)