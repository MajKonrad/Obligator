import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from canvas import get_future_assignment_deadlines, format_deadlines, get_exams
from resources import add_resource

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

@bot.command(help="Viser nærmeste kommende oblig-deadline")
async def nextdeadline(ctx):
    deadlines = get_future_assignment_deadlines()
    nextdeadline = deadlines[0]
    message = format_deadlines([nextdeadline])
    await ctx.send(f"⏰ **Nærmeste kommende deadline:**\n\n{message}")

@bot.command(help="Viser alle kommende Canvas-deadlines.")
async def deadlines(ctx):
    deadlines = get_future_assignment_deadlines()
    message = format_deadlines(deadlines)
    await ctx.send(message)

@bot.command(help="Viser kommende eksamener og mappeleveringer.")
async def exams(ctx):
    exams = get_exams()
    message = "📚 **Kommende eksamener og innleveringer**\n\n"

    for exam in exams:
        formatted_date = exam["date"].strftime("%d.%m.%Y kl. %H:%M")

        if exam["type"] == "Mappelevering":
            emoji = "📁"
        else:
            emoji = "📝"

        message += f"{emoji} **{exam['course']}**\n"
        message += f"{exam['type']}\n"
        message += f"{formatted_date}\n"

        if exam["duration"] is not None:
            message += f"{exam['duration']}\n"

        message += "\n"
    await ctx.send(message)


@bot.command()
async def help(ctx):
    message = "📚 **Obligator commands**\n\n"

    emojis = {
        "ping": "🏓",
        "deadlines": "📅",
        "nextdeadline": "⏰",
        "exams": "📝",
        "add": "➕"
    }

    for command in bot.commands:
        if command.name == "help":
            continue

        emoji = emojis.get(command.name, "🔹")

        message += (
            f"{emoji} **`!{command.name}`**\n"
            f"{command.help}\n\n"
        )
    await ctx.author.send(message)


@bot.command(
    help='Legger til en studieressurs.\nEksempel: !add DATS2300 "Binary Trees" "Bra forklaring på BST" https://youtube.com/...'
)
async def add(ctx, course, title, description, url):
    added_by = str(ctx.author)
    success = add_resource(course, title, description, url, added_by)
    if success:
        await ctx.send("✅ Ressursen ble lagt til!")
    else:
        await ctx.send("⚠️ Denne ressursen finnes allerede.")

bot.run(DISCORD_TOKEN)
