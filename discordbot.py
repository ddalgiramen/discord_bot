import discord
import os
from discord.ext import tasks
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}\n')
    loop.start()
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('<:ohajett:1059962614869938278>'):
        await message.add_reaction("<:ohajett:1059962614869938278>")
        print(message.author.id)


@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.now().strftime('%H:%M')
    if now == '07:30':
        channel = client.get_channel(1010108583670722590)
        await channel.send('<:ohajett:1059962614869938278>')

client.run(os.environ['TOKEN'])
