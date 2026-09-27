# Obligator

Obligator is a Discord bot that fetches upcoming assignment deadlines from Canvas and displays them in Discord.

## How it works

The bot connects to the Canvas API using a personal Canvas token and retrieves future assignments from selected courses.

Available commands:

- `!ping` — checks if the bot is online
- `!deadlines` — shows upcoming assignments sorted by deadline

Deadlines are converted to Oslo local time before being displayed.

## Installation

Install the required packages:

```bash
python3 -m pip install requests python-dotenv discord.py
```

Create a `.env` file in the project folder:

```env
CANVAS_TOKEN=your_canvas_token
DISCORD_TOKEN=your_discord_token
```

Make sure `.env` is ignored by Git:

```gitignore
.env
__pycache__/
*.pyc
.DS_Store
```

Run the bot:

```bash
python3 bot.py
```

The bot will remain online for as long as the Python process is running.