import lightbulb
import hikari
from asyncio import TimeoutError
import hashlib
import utils
import pin_db
from datetime import datetime

reference_plugin = lightbulb.Plugin('Reference')

@reference_plugin.command
@lightbulb.command('reference', 'Test command to learn about referenced messages.')
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def reference_command(ctx: lightbulb.context.Context) -> None:
    embed = hikari.Embed(
        title='Save Message',
        description='''Save a message to the pins channel by either responding
            with an exclamation mark followed by the message id, or replying
            directly to the message you want saved within the next 45 seconds.''',
        color=hikari.colors.Color(0xf5c71a)
    )
    await ctx.respond(embed=embed)
    try:
        with ctx.bot.stream(hikari.events.MessageCreateEvent, timeout=45).filter(('author_id', ctx.author.id)) as stream:
            async for event in stream:
                pin_db.save_to_database(ctx.bot, event.message.referenced_message)

                message_embed = hikari.Embed(
                    title='Saved Message.',
                    color=hikari.Color(0x0000b4),
                    description=event.message.referenced_message.content
                ).set_author(
                    name=event.message.referenced_message.author.username,
                    icon=event.message.referenced_message.author.avatar_url.url
                ).add_field(
                    name='Message ID',
                    value=f'[{event.message.referenced_message.id}]({event.message.referenced_message.make_link(ctx.get_guild().id)})',
                ).set_footer(
                    text=str(event.message.referenced_message.timestamp)
                )
                if len(event.message.referenced_message.attachments) > 0:
                    message_embed.set_image(event.message.referenced_message.attachments[0].url)
                    message_embed.add_field(
                        name='Attachments',
                        value='\n'.join(_format_attachment_urls(event.message.referenced_message.attachments))
                    )   

                await ctx.bot.rest.create_message(824102922332930068, embed=message_embed)

                success_embed = hikari.Embed(
                    title='Saved',
                    description='Message has been saved successfully.',
                    color=hikari.Color(0x66FF00)
                )
                await ctx.edit_last_response(embed=success_embed)
                await event.message.delete()

    except TimeoutError:
        timeout_embed = hikari.Embed(
            title='Save Canceled',
            description='45 seconds have elapsed, save canceled.',
            color=hikari.Color(0xdb0000)
        )
        await ctx.edit_last_response(embed=timeout_embed)

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(reference_plugin)

def get_attachments(attachments: []) -> str:
    if len(attachments) > 0:
        path_list = []
        for attachment in attachments:
            path_list.append(utils.save_file('./attachments/', ''.join([str(attachment.id), '_', attachment.filename]), attachment.url))
        return path_list

def _format_attachment_urls(attachments: []) -> []:
    if len(attachments) > 0:
        urls = []
        for attachment in attachments:
            urls.append(f'[{attachment.filename}]({attachment.url})')
        return urls