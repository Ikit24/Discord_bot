from discord.ext import commands, tasks
import discord
from dataclasses import dataclass

with open('token.txt', 'r') as f:
    BOT_TOKEN = f.read().strip()

CHANNEL_ID = 308289885767204864
MAX_SESSION_TIME_MINUTES = 30

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

@tasks.loop(minutes=MAX_SESSION_TIME_MINUTES, count=2)
async def break_reminder():
    if break_reminder.current_loop ==0:
        return

    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"**Take a break!** You've been studying for {MAX_SESSION_TIME_MINUTES} minutes.")

@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return

    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    break_reminder.start()
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

    break_reminder.stop()
    await ctx.send(f"Session ended after {formatted_duration}.")


bot.run(BOT_TOKEN)