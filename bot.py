from discord.ext import commands
import discord
from dataclasses import dataclass

with open('token.txt', 'r') as f:
    BOT_TOKEN = f.read().strip()

CHANNEL_ID = 308289885767204864

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
session = Session()

@bot.event
async def on_ready():
    print("Hello! Study bot is ready!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! Study bot is ready!")

@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return

    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    await ctx.send(f"New session started at {human_readable_time}")

@bot.command()
async def end(ctx):
    if not session.is_active:
        await ctx.send("No session is active!")
        return

    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration_seconds = end_time - session.start_time
    
    hours = int(duration_seconds // 3600)
    minutes = int((duration_seconds % 3600) //60)
    seconds = int(duration_seconds % 60)
    formatted_duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    await ctx.send(f"Session ended after {formatted_duration} seconds.")


bot.run(BOT_TOKEN)