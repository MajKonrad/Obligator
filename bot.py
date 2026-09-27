import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from canvas import get_future_assignment_deadlines, format_deadlines

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"{bot.user} er online!")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def deadlines(ctx):
    deadlines = get_future_assignment_deadlines()
    message = format_deadlines(deadlines)
    await ctx.send(message)

bot.run(DISCORD_TOKEN)
