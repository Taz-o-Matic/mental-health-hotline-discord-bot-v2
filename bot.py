import discord
from discord.ext import commands, tasks
import json
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

welcomed_users = set()

@bot.event
async def on_ready():
    print(f'✅ Bot is ready as {bot.user}')
    await load_hotlines_data()
    update_hotlines.start()
    
    try:
        guild = discord.Object(id=1507396942383284244)
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        print(f"✅ Successfully synced {len(synced)} commands")
    except Exception as e:
        print(f"Sync error: {e}")

async def load_hotlines_data():
    try:
        with open('hotlines.json', 'r', encoding='utf-8') as f:
            bot.hotlines_data = json.load(f)
        print(f"✅ Loaded {len(bot.hotlines_data.get('countries', {}))} countries")
    except Exception as e:
        print(f"❌ Error loading hotlines.json: {e}")
        bot.hotlines_data = {"countries": {}}

@tasks.loop(hours=6)
async def update_hotlines():
    print("🔄 Refreshing hotline data...")
    await load_hotlines_data()

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.name == "help-lines":
        if message.author.id not in welcomed_users:
            welcomed_users.add(message.author.id)
            embed = discord.Embed(title="🆘 Welcome to Mental Health Support", color=0x00b4d8)
            embed.description = f"Hey {message.author.mention}! 👋\n\nThis is a **safe and private** space."
            embed.add_field(name="How to get help", value="`/help` - Show commands\n`/hotline` - Get hotlines\n`/list_countries` - See countries\n`/crisis` - Emergency help", inline=False)
            embed.set_footer(text="You are not alone • All messages are private")
            await message.channel.send(embed=embed)

    await bot.process_commands(message)

async def load_cogs():
    await bot.load_extension("cogs.hotlines")

async def main():
    await load_cogs()
    await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())