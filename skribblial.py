from logging import fatal
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

@bot.command(name='close', brief='Shuts down the bot')
async def close(ctx):
    await ctx.message.delete()
    await bot.close()

@bot.command(name='redo', brief='Compresses all words into one message')
async def redo(ctx):
    await ctx.message.delete()
    word_lst = await get_word_list(await ctx.channel.history(limit=200).flatten())
    await create_messages(word_lst, ctx)

@bot.command(name='add', brief='Adds the given words to the list')
async def add(ctx, *args):
    await ctx.message.delete()
    word_lst = await get_word_list(await ctx.channel.history(limit=200).flatten())
    for arg in args:
        if arg not in word_lst and len(arg) < 31 and "'" not in arg:
                word_lst.append(arg)
    await create_messages(word_lst, ctx)

@bot.command(name='rm', brief='Removes the given words from the list')
async def remove(ctx, *args):
    await ctx.message.delete()
    word_lst = await get_word_list(await ctx.channel.history(limit=200).flatten())
    for arg in args:
        if arg in word_lst:
            word_lst.remove(arg)
    await create_messages(word_lst, ctx)

@bot.command(name='ng', brief='Replaces the game link with a new one')
async def new_game(ctx, arg):
    await ctx.message.delete()
    messages = await ctx.channel.history(limit=200).flatten()
    for msg in messages:
        if "Skribblial" in msg.content:
            await discord.Message.delete(msg)
    await ctx.send("Skribblial : " + arg)

@bot.command(name='ping', brief='Pings the funny fellows')
async def ping(ctx):
    await ctx.message.delete()
    messages = await ctx.channel.history(limit=200).flatten()
    for msg in messages:
        if "@here" in msg.content:
            await discord.Message.delete(msg)
    await ctx.send("@here viendez bande de gens")

async def get_word_list(messages):
    word_lst = []

    for msg in messages:
        if "||" in msg.content:
            word_lst.extend(msg.content.replace("||", '').split(", "))
            await msg.delete()

    return word_lst

async def create_messages(words, ctx):
    msg = "||" + words[0]
    for word in words[1:]:
        if (len(msg) + len(word) + 2) >= 1990:
            msg += "||"
            await ctx.send(msg)
            msg = "||" 
        msg += ", " + word

    msg += "||"
    await ctx.send(msg)

bot.run(TOKEN)