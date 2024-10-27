import discord
from discord.ext import commands, tasks
import asyncio
import datetime

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Specify the ID of the channel to send the check-in message to
channel_id = 1299877289869180962  # Replace with your channel ID

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    daily_checkin.start()  # Start the daily check-in task

# Schedule the check-in to run daily at a specific time
@tasks.loop(hours=24)
async def daily_checkin():
    await bot.wait_until_ready()  # Ensure the bot is ready
    channel = bot.get_channel(channel_id)

    # Get current time and wait until 10:00 AM
    now = datetime.datetime.now()
    target_time = now.replace(hour=10, minute=0, second=0, microsecond=0)
    if now > target_time:
        target_time += datetime.timedelta(days=1)  # Schedule for next day if past 10:00 AM

    wait_time = (target_time - now).total_seconds()
    await asyncio.sleep(wait_time)

    # Send the check-in message to the channel
    message = await channel.send(
        "Mental health check-in:\n\n"
        "❤️ - I’m good\n"
        "💙 - I could be better\n"
        "🖤 - I’m struggling"
    )
    await message.add_reaction("❤️")
    await message.add_reaction("💙")
    await message.add_reaction("🖤")

# Listen for reactions to the check-in message
@bot.event
async def on_reaction_add(reaction, user):
    # Ensure bot doesn't respond to its own reactions
    if user == bot.user:
        return

    # Check if reaction is to the check-in message and is the black heart (🖤)
    if reaction.message.channel.id == channel_id and str(reaction.emoji) == "🖤":
        # Post a message tagging the user who reacted with 🖤
        await reaction.message.channel.send(
            f"{user.mention} is struggling. Admins and members, please reach out to support them. 🖤"
        )

# Add a command to trigger the check-in manually
@bot.command(name='checkin')
async def manual_checkin(ctx):
    channel = bot.get_channel(channel_id)
    if channel is not None:
        message = await channel.send(
            "Mental health check-in:\n\n"
            "❤️ - I’m good\n"
            "💙 - I could be better\n"
            "🖤 - I’m struggling"
        )
        await message.add_reaction("❤️")
        await message.add_reaction("💙")
        await message.add_reaction("🖤")
    else:
        await ctx.send("Check-in channel not found.")

# Run the bot
bot.run("TOKEN")
