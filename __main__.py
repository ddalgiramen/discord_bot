#import Discord relation
import discord
from discord.ext import tasks

#import env
import os
from dotenv import load_dotenv

#import date and DB
from datetime import datetime, timedelta, timezone
import sqlite3

#loading .env file
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
JST = timezone(timedelta(hours=+9), 'JST')
client = discord.Client(intents=intents)


GENERAL_CH_ID = 1010108583670722590
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}\n')
    loop.start()

@client.event
async def on_message(message):
    if message.content.startswith('<:ohajett:1059962614869938278>') and message.channel.id == GENERAL_CH_ID:
        conn = sqlite3.connect("counts.db")
        today = datetime.now(JST).date()
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS counts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                counter INTEGER,
                created_at DATE NOT NULL
            )
        """)
        result = c.execute("""
            SELECT * FROM counts WHERE id=?
        """, (str(message.author.id),)).fetchone()

        if result is not None:
            stamp = datetime.strptime(result[3], '%Y-%m-%d')

        # check if the user has already made a count today
        if result is None:
            print("INSERT")
            # add a new count for the user
            c.execute("""
                INSERT INTO counts (id, username, counter, created_at)
                VALUES (?, ?, ?, ?)
            """, (str(message.author.id), str(message.author.name), 1, today))
            await message.add_reaction("<:ohajett:1059962614869938278>")
        elif stamp.date() != today:
            # update the count for the user
            c.execute("""
                UPDATE counts SET counter=?, created_at=? WHERE id=?
            """, (result[2] + 1, today, str(message.author.id)))

            await message.add_reaction("<:ohajett:1059962614869938278>")
        else:
            print("NOTHING")
            # the user has already counted today
            await message.channel.send("You have already counted today. Please try again tomorrow.")
        conn.commit()
        conn.close()
    elif message.content.startswith('<:ohajett:1059962614869938278>') and message.channel.id != GENERAL_CH_ID:
        await message.add_reaction("<:ohajett:1059962614869938278>")

    if message.content.startswith("!show_count"):
        conn = sqlite3.connect('counts.db')
        c = conn.cursor()

        result = c.execute("""
            SELECT * FROM counts WHERE id=?
        """, (str(message.author.id),)).fetchone()

        if result:
            text = f'hi!{result[1]}. Your attendance is {result[2]}'
            await message.channel.send(text)
        else:
            await message.channel.send("There is no data.")
        conn.close()
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.now(JST).strftime('%H:%M')
    if now == '07:30':
        channel = client.get_channel(1010108583670722590)
        await channel.send('<:ohajett:1059962614869938278>')

client.run(os.environ['TOKEN'])