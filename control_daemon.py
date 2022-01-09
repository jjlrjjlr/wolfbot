from aioconsole import ainput
import hikari
import lightbulb
import sys
import asyncio
import logging
import time

logging.getLogger()


class CommandRegistry:
    _commands = {}

    @classmethod
    def register(cls, *args):
        def decorator(fn) -> 'function':
            cls._commands[fn.__name__] = fn
            return fn
        return decorator

    @classmethod
    async def execute(cls, command, ctx) -> None:
        if command in cls._commands:
            await cls._commands[command](ctx)
        else:
            logging.warning(f'{command} is not a valid command. Please enter a valid command, or type "help" for a list of commands.')

@CommandRegistry.register()
async def exit(ctx: dict) -> None:
    print(ctx)
    await ctx['bot'].close()
    asyncio.get_event_loop().stop()

@CommandRegistry.register()
async def help(ctx: dict) -> None:
    pass

async def prompt(bot: lightbulb.BotApp) -> None:
    await asyncio.sleep(3)
    while True:
        user_input = await ainput('> ')
        if user_input not in [None, '']:
            split_input = user_input.split()
            print(user_input, '\n', split_input)
            await CommandRegistry.execute(
                split_input[0],
                {
                    'command': split_input[0],
                    'args': split_input[1:],
                    'raw_command': user_input,
                    'bot': bot
                }
            )


async def tests() -> None:
    print(CommandRegistry._commands)
    await prompt('test_bot')

if __name__ == '__main__':
    print(CommandRegistry._commands)