import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from canvas import get_future_assignment_deadlines, format_deadlines, get_exams
from progress import mark_completed, mark_undone


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

@bot.command(help="Markerer en deadline som ferdig. Eksempel: !done 2")
async def done(ctx, number: int):
    deadlines = get_future_assignment_deadlines()
    if number < 1 or number > len(deadlines):
        await ctx.send("❌ Ugyldig nummer. Sjekk `!deadlines` for tilgjengelige deadlines.")
        return
    assignment = deadlines[number - 1]
    mark_completed(assignment["assignment_id"])
    await ctx.send(f"✅ {assignment['name']} er markert som ferdig!")

@bot.command(help="Fjerner ferdig-markering fra en deadline. Eksempel: !undone 2")
async def undone(ctx, number: int):
    deadlines = get_future_assignment_deadlines()
    if number < 1 or number > len(deadlines):
        await ctx.send("❌ Ugyldig nummer. Sjekk `!deadlines` for tilgjengelige deadlines.")
        return
    assignment = deadlines[number - 1]
    mark_undone(assignment["assignment_id"])
    await ctx.send(f"⬜ {assignment['name']} er markert som ikke ferdig!")

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
        "add": "➕",
        "done": "✅",
        "undone": "⬜"
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

bot.run(DISCORD_TOKEN)
