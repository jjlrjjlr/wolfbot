import lightbulb
import hikari
from asyncio import TimeoutError
import hashlib
import utils
import pin_db
from datetime import datetime
import traceback
import logging
import log_formatter
from sys import argv
import time

logging.getLogger()

pin_plugin = lightbulb.Plugin('Pin')

@pin_plugin.command
@lightbulb.option('message_url', 'URL of the message to save.', required=False, type=str)
@lightbulb.command('pin', 'Save a message to the pins channel and to the pins database.')
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def pin_command(ctx: lightbulb.context.Context) -> None:
    if ctx.bot.d.settings.get_save_channel(ctx.get_guild().id) == -1:
        await ctx.respond(
            embed=hikari.Embed(
                title='Warning',
                description='You have not specified a channel to save pins to, please specify one with /settings to use this command.',
                color=hikari.Color(0xffff00)
            )
        )
    else:
        if ctx.options.message_url is not None and ctx.options.message_url.startswith('https://'):
            split_url = ctx.options.message_url.split('/')
            _guild, _channel, _message = split_url[4:7]
            logging.debug(f'\n\tURL: {ctx.options.message_url}\n\tChannel: {_channel}\n\tMessage: {_message}')

            if int(_guild) != ctx.get_guild().id:
                logging.warning(f'{ctx.author.username}:{ctx.author.id} attempted to save a message from {_guild} in {ctx.get_guild().id}.')
                await ctx.respond(
                    embed=hikari.Embed(
                        title='Warning',
                        description='Cross guild message saving is not supported,\
                             if you wish to save a message please make sure to do so\
                            from within the guild the message exists.',
                        color=hikari.Color(0xffff00)
                    )   
                )
                return
            
            try:
                message = await ctx.bot.rest.fetch_message(int(_channel), int(_message))
                
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

                logging.info(f'Message {_guild}:{_channel}:{_message} saved by user {ctx.author.username}:{ctx.author.discriminator}:{ctx.author.id}')
            except Exception as e:
                logging.exception('Unknown exception when attempting to save message through "message_url" option.' )
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
                        want saved with the word "save" within the next 45
                        seconds, or say "cancel" to cancel this request.''',
                    color=hikari.colors.Color(0xf5c71a)
                )
            )
            try:
                with ctx.bot.stream(hikari.events.MessageCreateEvent, timeout=45).filter(('author_id', ctx.author.id)) as stream:
                    event: hikari.events.MessageCreateEvent
                    stream: hikari.api.EventStream
                    async for event in stream.limit(1):
                        if event.message.content == 'save':
                            pin_db.save_to_database(ctx.bot, event.message.referenced_message)

                            await ctx.bot.rest.create_message(
                                ctx.bot.d.settings.get_save_channel(ctx.guild_id.real),
                                embed=build_message_embed(event.message.referenced_message, ctx.get_guild().id.real)
                            )

                            logging.info(f'Message {ctx.get_guild().id}:{ctx.get_channel().id}:{event.message.referenced_message.id} saved by user {ctx.author.username}:{ctx.author.discriminator}:{ctx.author.id}')

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
        name='ID:',
        value=f'[{message.id}]({message.make_link(guild_id)})',
    ).add_field(
        name='Sent:',
        value=f'<t:{int(time.mktime(message.timestamp.timetuple()))}>',
        inline=True
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