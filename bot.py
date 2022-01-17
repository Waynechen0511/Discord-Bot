import discord
from discord.ext import commands
from modules.ahttp import AIOHTTP
from dotenv import load_dotenv
import os
import random

load_dotenv()
TOKEN = os.environ.get("TOKEN")

bot = commands.Bot(command_prefix = '.')

# Reloads a cog
@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
  bot.unload_extension(f"cogs.{extension}")
  bot.load_extension(f"cogs.{extension}")
  await ctx.send(extension + " successfuly reloaded")

# Goes through the /cogs folder and loads all of the python cogs in it
for filename in os.listdir("./cogs"):
  if filename.endswith(".py"):
    bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  await bot.process_commands(message)

@bot.event
async def invalid_command(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    await ctx.send("Invalid command")

@bot.command()
async def choose(ctx, *, arg):
  choices = arg.split(", ")
  ran = random.randrange(len(choices))
  await ctx.send(choices[ran])  

@reload.error
async def reload_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.reply("You do not have permissions to reload Cogs.")

bot.run(TOKEN)
