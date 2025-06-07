from discord.ext import commands, tasks
import discord, random
from dataclasses import dataclass

with open('token.txt', 'r') as f:
    BOT_TOKEN = f.read().strip()

CHANNEL_ID = 308289885767204864
MAX_SESSION_TIME_MINUTES = 30

greetings = [
    "Hey there! How’s it going?",
    "Hi! Great to see you!",
    "Hello! Hope you’re having a good day.",
    "Hey! What’s new with you?",
    "Hi there! Long time no see.",
    "Good to see you! How have you been?",
    "Hey! How are things?",
    "Hello! Everything okay on your end?",
    "Hi! What’s been keeping you busy?",
    "Hey, hey! How’s life treating you?",
    "Hi! Nice to hear from you.",
    "Hello there! What’s going on?",
    "Hey! How’s your day shaping up?",
    "Hiya! All good with you?",
    "Yo! What’s happening?",
    "Hey! Feeling good today?",
    "Hi! Got time for a quick chat?",
    "Hello! Been thinking about you.",
    "Hey there! What’s on your mind?",
    "Hi! Let’s catch up soon."
]

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

@bot.command(name="hello")
async def greeting(ctx):
    random_greeting = random.choice(greetings)

    await ctx.send(random_greeting)


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