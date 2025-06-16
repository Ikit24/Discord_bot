from discord.ext import commands, tasks
import discord, random
from dataclasses import dataclass

with open('token.txt', 'r') as f:
    BOT_TOKEN = f.read().strip()

CHANNEL_ID = 308289885767204864
MAX_SESSION_TIME_MINUTES = 30

greeting_responses = {
    'hello':["Hello! 👋", "Hi there!", "Hey!", "Greetings!"],
    'hi': ["Hello! 👋", "Hi there!", "Hey!", "Greetings!"],
    'morning': ["Good morning! ☀️", "Morning!", "Rise and shine!", "Top of the morning!"],
    'evening': ["Good evening! 🌙", "Evening!", "Hope you had a great day!"],
    'sup': ["Sup! 😎", "Yo!", "What's good?", "Ayy!"],
    'bye': ["See ya! 👋", "Goodbye!", "Take care!", "Catch you later!"]
}

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
    if channel:
        try:
            await channel.send("Hello! Study bot is ready!")
        except discord.errors.Forbidden:
            print("Bot doesn't have permission to send to this channel")
    else:
        print("Channel not found")

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(random.choice(greeting_responses['hello']))

@bot.command(name='hi')
async def hi(ctx):
    await ctx.send(random.choice(greeting_responses['hi']))

@bot.command(name='morning')
async def morning(ctx):
    await ctx.send(random.choice(greeting_responses['morning']))

@bot.command(name='evening')
async def evening(ctx):
    await ctx.send(random.choice(greeting_responses['evening']))

@bot.command(name='sup')
async def sup(ctx):
    await ctx.send(random.choice(greeting_responses['sup']))

@bot.command(name='bye')
async def bye(ctx):
    await ctx.send(random.choice(greeting_responses['bye']))  


@tasks.loop(minutes=MAX_SESSION_TIME_MINUTES, count=2)
async def break_reminder():
    if break_reminder.current_loop == 0:
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

async def auto_end_poll(message_id, duration_seconds):
    await asyncio.sleep(duration_seconds)

    if message_id not in active_polls:
        return

    poll_data = active_polls[message_id]
    channel = bot.get_channel(poll_data['channel'])
    poll_message = await channel.fetch_message(message_id)

    emojis = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯']

    results_text = f"**⏰ POLL ENDED: {poll_data['question']}**\n\n"
    vote_counts = []

    for i, option in enumerate(poll_data['options']):
        count = 0
        for reaction in poll_message.reactions:
            if str(reaction_emoji) == emojis[i]:
                count = reaction.count - 1
                break
        results_text += f"• {option}: {count} votes\n"
        vote_counts.append(count)

    winner_index = vote_counts.index(max(vote_counts))
    winner_option = poll_data['options'][winner_index]
    results_text += f"\n🏆 **Winner: {winner_option}**"

    await channel.send(results_text)
    del active_polls[message_id]

active_polls = {}
@bot.command()
async def create_poll(ctx, *, args):
    parts = [part.strip() for part in args.split('|')]

    if len(parts) < 3:
        await ctx.send("Format: `!create_poll Question? | Option 1| Option 2 | Option 3`")
        return

    question = parts [0]

    try:
        duration = int(parts[-1])
        options = parts[1:-1]
        timed = True
    except ValueError:
        options = parts[1:]
        duration = None
        timed = False
    
    if not question.strip():
        await ctx.send("Question cannot be empty!")
        return
    
    if len(options) > 20:
        await ctx.send("Too many options! Max 20 reactions allowed!")
        return

    poll_text = f"**{question}**\n\n"

    emojis = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', 
              '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶', '🇷', '🇸', '🇹']

    for i, option in enumerate(options):
        poll_text += f"{emojis[i]} {option}\n"

    if timed:
        poll_text += f"\n⏰ **Poll ends in {duration} minutes**"

    poll_message = await ctx.send(poll_text)

    for i in range(len(options)):
        await poll_message.add_reaction(emojis[i])
    
    active_polls[poll_message.id] = {
        'question': question,
        'options': options,
        'channel': ctx.channel.id,
        'creator': ctx.author.id,
        'timed': timed,
        'duration': duration
    }    
    
    if timed:
        asyncio.create_task(auto_end_poll(poll_message.id, duration * 60))

@bot.command()
async def poll_results(ctx, message_id: int):
    if message_id not in active_polls:
        await ctx.send("Poll not found!")
        return
    
    poll_data = active_polls[message_id]
    channel = bot.get_channel(poll_data['channel'])
    poll_message = await channel.fetch_message(message_id)
    
    emojis = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', 
              '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶', '🇷', '🇸', '🇹']
    
    results_text = f"**Poll Results: {poll_data['question']}**\n\n"
    vote_counts = []
    
    for i, option in enumerate(poll_data['options']):
        count = 0
        for reaction in poll_message.reactions:
            if str(reaction.emoji) == emojis[i]:
                count = reaction.count - 1
                break
        results_text += f"• {option}: {count} votes\n"
        vote_counts.append(count)
    
    if vote_counts and max(vote_counts) > 0:
        winner_index = vote_counts.index(max(vote_counts))
        winner_option = poll_data['options'][winner_index]
        results_text += f"\n🏆 **Winner: {winner_option}**"
    
    await ctx.send(results_text)

@bot.command()
async def list_polls(ctx):
    if not active_polls:
        await ctx.send("No active polls")
        return

    for message_id, poll_data in active_polls.items():
        await ctx.send(f"Poll ID: {message_id} - Question: {poll_data['question']}")

@bot.command()
async def end_poll(ctx, message_id: int):
   if message_id not in active_polls:
       await ctx.send("Poll not found!")
       return
   
   poll_data = active_polls[message_id]
   
   if poll_data['creator'] != ctx.author.id:
       await ctx.send("Only the poll creator can end this poll!")
       return
   
   channel = bot.get_channel(poll_data['channel'])
   poll_message = await channel.fetch_message(message_id)
   
   emojis = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯']
   
   results_text = f"**Poll Results: {poll_data['question']}**\n\n"
   vote_counts = []
   
   for i, option in enumerate(poll_data['options']):
       count = 0
       for reaction in poll_message.reactions:
           if str(reaction.emoji) == emojis[i]:
               count = reaction.count - 1
               break
       results_text += f"• {option}: {count} votes\n"
       vote_counts.append(count)
   
   winner_index = vote_counts.index(max(vote_counts))
   winner_option = poll_data['options'][winner_index]
   results_text += f"\n🏆 **Winner: {winner_option}**"
   
   await ctx.send(results_text)
   
   del active_polls[message_id] 

bot.run(BOT_TOKEN)
