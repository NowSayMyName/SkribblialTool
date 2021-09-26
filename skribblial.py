import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

@bot.command(name='close')
async def close(ctx):
    await ctx.message.delete()
    await bot.close()

@bot.command(name='add')
async def add(ctx, *args):
    await ctx.message.delete()
    if len(args) < 1:
        await ctx.send("expected command: !add \"word\" ...")
    else:
        word_lst = await get_word_list(await ctx.channel.history(limit=200).flatten())
        word_lst.extend(x for x in args if x not in word_lst)
        await ctx.send(create_word_list(word_lst))

@bot.command(name='rm')
async def remove(ctx, *args):
    await ctx.message.delete()
    if len(args) < 1:
        await ctx.send("expected command: !rm \"word\" ...")
    else:
        word_lst = await get_word_list(await ctx.channel.history(limit=200).flatten())
        await ctx.send(create_word_list(word for word in word_lst if word not in args))


@bot.command(name='ng')
async def new_game(ctx, arg):
    await ctx.message.delete()
    messages = await ctx.channel.history(limit=200).flatten()
    for msg in messages:
        if "Skribblial" in msg.content:
            await discord.Message.delete(msg)
    await ctx.send("Skribblial : " + arg)


async def get_word_list(messages):
    word_lst = []

    for msg in messages:
        if "||" in msg.content:
            word_lst.extend(msg.content.replace("||", '').split(", "))
            await msg.delete()

    return word_lst

def create_word_list(words):
    msg = "||"
    msg += words[0]
    for word in words[1:]:
        msg += ", " + word
    msg += "||"

    return msg

bot.run(TOKEN)