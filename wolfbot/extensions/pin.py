import lightbulb
import hikari
from asyncio import TimeoutError
import hashlib
import utils
import pin_db
from datetime import datetime
import traceback

pin_plugin = lightbulb.Plugin('Pin')

@pin_plugin.command
@lightbulb.option('channel', 'ID of the channel the message to save is in. This must be used with the `Message` option.', required=False)
@lightbulb.option('message', 'ID of the message to save. This must be used with the `Channel` option.', required=False)
@lightbulb.command('pin', 'Save a message to the pins channel and to the pins database.')
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def pin_command(ctx: lightbulb.context.Context) -> None:
    if ctx.options.channel is not None and ctx.options.message is not None:
        try:
            message = await ctx.bot.rest.fetch_message(int(ctx.options.channel), int(ctx.options.message))
            
            pin_db.save_to_database(ctx.bot, message)

            await ctx.bot.rest.create_message(
                ctx.bot.d.settings.get_save_channel(ctx.guild_id.real),
                embed=build_message_embed(message, ctx.get_guild().id.real)
            )

            await ctx.respond(
                embed=hikari.Embed(
                    title='Saved',
                    description=f'[Message]({message.make_link(ctx.get_guild().id)}) has been saved successfully.',
                    color=hikari.Color(0x66FF00)
                )
            )
        except Exception as e:
            print(traceback.format_exc())
            await ctx.respond(
                embed=hikari.Embed(
                    title='Error',
                    description=e,
                    color=hikari.Color(0x660000)
                )
            )
    else:
        await ctx.respond(
            embed=hikari.Embed(
                title='Save Message',
                description='''Save a message to the pins channel by
                    replying directly to the message you
                    want saved within the next 45 seconds.''',
                color=hikari.colors.Color(0xf5c71a)
            )
        )
        try:
            with ctx.bot.stream(hikari.events.MessageCreateEvent, timeout=45).filter(('author_id', ctx.author.id)) as stream:
                event: hikari.events.MessageCreateEvent
                async for event in stream:
                    if event.message.content == 'save':
                        pin_db.save_to_database(ctx.bot, event.message.referenced_message)

                        await ctx.bot.rest.create_message(
                            ctx.bot.d.settings.get_save_channel(ctx.guild_id.real),
                            embed=build_message_embed(event.message.referenced_message, ctx.get_guild().id.real)
                        )

                        await ctx.edit_last_response(
                            embed=hikari.Embed(
                                title='Saved',
                                description='Message has been saved successfully.',
                                color=hikari.Color(0x66FF00)
                            )
                        )
                    
                    elif event.message.content == 'cancel':
                        await ctx.edit_last_response(
                            embed=hikari.Embed(
                                title='Canceled',
                                description='Pin canceled.',
                                color=hikari.Color(0x660000)
                            )
                        )
                    
                    elif event.message.content not in [None, ''] and ':' in event.message.content:
                        message_location = event.message.content.split(':')
                        message: hikari.messages.Message

                        try:
                            message = await ctx.bot.rest.fetch_message(message_location[0], message_location[1])
                        except Exception as e:
                            print(traceback.format_exc())
                            await ctx.edit_last_response(
                                embed=hikari.Embed(
                                    title='Error',
                                    description=e,
                                    color=hikari.Color(0x660000)
                                )
                            )
                        
                        pin_db.save_to_database(ctx.bot, message)

                        await ctx.bot.rest.create_message(
                            ctx.bot.d.settings.get_save_channel(ctx.guild_id.real),
                            embed=build_message_embed(message, ctx.get_guild().id.real)
                        )

                        await ctx.edit_last_response(
                            embed=hikari.Embed(
                                title='Saved',
                                description='Message has been saved successfully.',
                                color=hikari.Color(0x66FF00)
                            )
                        )

                    else:
                        await ctx.edit_last_response(
                            embed=hikari.Embed(
                                title='Error',
                                description='Invalid response.',
                                color=hikari.Color(0x660000)
                            )
                        )

                    await event.message.delete()
            

        except TimeoutError:
            timeout_embed = hikari.Embed(
                title='Save Canceled',
                description='45 seconds have elapsed, save canceled.',
                color=hikari.Color(0xdb0000)
            )
            await ctx.edit_last_response(embed=timeout_embed)


def build_message_embed(message: hikari.messages.Message, guild_id: int) -> hikari.Embed:
    message_embed = hikari.Embed(
        title='Saved Message.',
        color=hikari.Color(0x0000b4),
        description=message.content
    ).set_author(
        name=message.author.username,
        icon=message.author.avatar_url.url
    ).add_field(
        name='Message ID',
        value=f'[{message.id}]({message.make_link(guild_id)})',
    ).set_footer(
        text=str(message.timestamp)
    )
    if len(message.attachments) > 0:
        message_embed.set_image(message.attachments[0].url)
        message_embed.add_field(
            name='Attachments',
            value='\n'.join(_format_attachment_urls(message.attachments))
        )
    return message_embed


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(pin_plugin)


def _format_attachment_urls(attachments: []) -> [str]:
    if len(attachments) > 0:
        urls = []
        for attachment in attachments:
            urls.append(f'[{attachment.filename}]({attachment.url})')
        return urls