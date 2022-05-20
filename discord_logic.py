import json
import os
import platform
import random
import nest_asyncio
import sys
import re
import asyncio

import requests_html
from dotenv import load_dotenv

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot

from telethon import TelegramClient, events

load_dotenv()
client = discord.Client()
intents = discord.Intents.default()
bot = Bot(command_prefix='$', intents=intents)

#Discord Channel
shitcoin = 909245601504456755

#HTML Thing
asession = requests_html.AsyncHTMLSession()

# BOT SETUP -> https://vcokltfre.dev/tutorial/12-errors/
class ErrorHandler(commands.Cog):
    """A cog for global error handling."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot


def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))

# CUSTOM FUNCTIONS

async def get_website(url: str):
    r = await asession.get(url)
    await r.html.arender(sleep=10)  # sleeping is optional but do it just in case
    html = r.html.raw_html  # this can be returned as your result
    await asession.close()  # this part is important otherwise the Unwanted Kill.Chrome Error can Occur
    # r.aclose()
    return r.html.arender

async def contract_check(contractaddr: str):
    url = f'https://honeypot.is/?address={contractaddr}'
    url_busd = f'https://honeypot.is/busd.html?address={contractaddr}'

    # ASYNC2
    # asession = requests_html.AsyncHTMLSession()
    r = await asession.get(url)
    await r.html.arender(sleep=10)  # sleeping is optional but do it just in case
    # await asession.close()  # this part is important otherwise the Unwanted Kill.Chrome Error can Occur

    # Do ya'thang
    _all1 = r.html.xpath('//*[@id="shitcoin"]/div//p/text()')

    if "unable" in _all1:
        r = await asession.get(url)
        await r.html.arender(sleep=10)
        # Do ya'thang
        _all1 = r.html.xpath('//*[@id="shitcoin"]/div//p/text()')

    _final_text = '---- ---- ---- ---- ---- \n'

    if len(_all1) == 7:
        print_order = [2, 1, 0, 3, 4, 5, 6]
        print(_all1)
        for p in print_order:
            _final_text = _final_text + _all1[p] + " \n"
        _final_text = _final_text + f'https://poocoin.app/tokens/{contractaddr}' + " \n"
    elif len(_all1) == 8:
        print_order = [2, 1, 0, 3, 4, 5, 6, 7]
        print(_all1)
        for p in print_order:
            _final_text = _final_text + _all1[p] + " \n"
        _final_text = _final_text + f'https://poocoin.app/tokens/{contractaddr}' + " \n"
    else:
        for p in range(len(_all1)):
            _final_text = _final_text + _all1[p] + " \n"
        _final_text = _final_text + f'https://poocoin.app/tokens/{contractaddr}' + " \n"

    return(_final_text)

# CUSTOM COMMANDS SET UP (LISTENERS?)

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.bot = bot
        self.shoutout.start()
        self._cached_stamp = 0
        self.filename = 'contracts.txt'

    def cog_unload(self):
        self.shoutout.cancel()

    def file_lines(self):
        f = open(self.filename)
        lines = 0
        buf_size = 1024 * 1024
        read_f = f.read  # loop optimization

        buf = read_f(buf_size)
        while buf:
            lines += buf.count('\n')
            buf = read_f(buf_size)

        f.close()
        return lines

    @tasks.loop(seconds=1.0)
    async def shoutout(self):
        stamp = os.stat(self.filename).st_mtime
        if stamp != self._cached_stamp:
            num_lines = MyCog.file_lines(self)
            # print("FileStamp")
            # print(num_lines)
            if num_lines > 0:
                # try:
                self._cached_stamp = stamp
                # File has changed, so do something...
                f = open(self.filename, "r")
                content_list = f.readlines()
                f.close()
                channel = bot.get_channel(shitcoin)  # Gets channel from internal cache
                for contract in content_list:
                    await channel.send(f"$ctc {contract}")  # Sends message to channel

                with open(self.filename, 'w'): pass
                stamp = os.stat(self.filename).st_mtime
                self._cached_stamp = stamp
                # except:
                #     print("error al leer contratos")

    @shoutout.before_loop
    async def before_shoutout(self):
        # print('waiting...')
        await self.bot.wait_until_ready()



@bot.event
async def on_message(message):
    # print("entro on_message")
    # print(message.content)
    if message.channel.id == shitcoin:
        # print("canal shitcoin")
        _author = str(message.author)
        # Ignores if a command is being executed by a bot or by the bot itself
        if "bschoneypot" in _author:
            # print("envio bot")
            if message.content.find("$ctc") == -1:
                # print("no es ctc")
                return
            if message.content.find("$ctc") >= -1:
                # print("es CTC")
                arg = re.findall(r'(0x\w+)', message.content)
                _response = await contract_check(arg[0])
                channel = bot.get_channel(shitcoin)  # Gets channel from internal cache
                await message.delete()
                await channel.send(_response)  # Sends message to channel

    await bot.process_commands(message)

@bot.command(name='ctc', help='Revisa si el contrato es un honeypot.')
async def ctc(ctx, *, arg: str):
    if len(arg) != 42:
        message = "¿El contrato está bien escrito? (n!=42)"
        await ctx.send(message, delete_after=5)
        await ctx.message.delete(delay=5)
        return

    _is_valid_contract = re.fullmatch(r'^0x\w*', arg)
    if _is_valid_contract == None:
        message = "¿El contrato está bien escrito? (regexp fail)"
        await ctx.send(message, delete_after=5)
        await ctx.message.delete(delay=5)
        return

    message = "Obteniendo información..."
    await ctx.send(message, delete_after=20)
    # await ctx.message.delete(delay=20)
    _response = await contract_check(arg)
    await ctx.send(_response)

@bot.command(name='test')
async def test(ctx, *args):
    await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))

# The code in this even is executed when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")

# ERROR HANDLER
@commands.Cog.listener()
async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
    """A global error handler cog."""

    if isinstance(error, commands.CommandNotFound):
        return  # Return because we don't want to show an error for every command not found
    elif isinstance(error, commands.CommandOnCooldown):
        message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
    elif isinstance(error, commands.MissingPermissions):
        message = "You are missing the required permissions to run this command!"
    elif isinstance(error, commands.UserInputError):
        message = "Something about your input was wrong, please check your input and try again!"
    else:
        message = "Oh no! Something went wrong while running the command!"

    await ctx.send(message, delete_after=5)
    await ctx.message.delete(delay=5)

# BOT COMMANDS LIST
# bot.add_command(test)

# cogs
bot.add_cog(MyCog(bot))


# RUN MODAFOCA
bot.run(os.getenv('TOKEN'))