import discord
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

f = open("channel_id.txt", "w")

client = discord.Client(intents=intents)
@client.event
async def on_ready():
    for ch in client.get_all_channels():
        f.write("--------------------\n")
        f.write("channel_name:\n")
        f.write(str(ch.name)+"\n")
        f.write("channel_id:%s\n")
        f.write(str(ch.id)+"\n")
        f.write("-----------------------\n")
    print("fin")

client.run(os.environ['TOKEN'])
