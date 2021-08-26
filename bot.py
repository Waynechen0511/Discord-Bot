import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random

load_dotenv()
TOKEN = os.environ.get("TOKEN")

bot = commands.Bot(command_prefix = '.')


@bot.command()
async def load(ctx, extension):
  bot.load_extension(f"cogs.{extension}")

@bot.command()
async def unload(ctx, extension):
  bot.unload_extension(f"cogs.{extension}")

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

bot.run(TOKEN)