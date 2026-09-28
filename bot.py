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
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print(f"{bot.user} er online!")

@bot.command(help="Sjekker om boten er online.")
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command(help="Viser alle kommende Canvas-deadlines.")
async def deadlines(ctx):
    deadlines = get_future_assignment_deadlines()
    message = format_deadlines(deadlines)
    await ctx.send(message)

@bot.command()
async def help(ctx):
    message = "📚 Obligator commands:\n\n"
    for command in bot.commands:
        message += f"!{command.name} - {command.help}\n"
    await ctx.author.send("Hei")

bot.run(DISCORD_TOKEN)
