# bot.py
import os
import discord
import random

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.typing = True
client = discord.Client(intents=intents)
ogmaps = ['Afghan','Derail','Estate','Favela','Highrise','Invasion','Karachi','Quarry','Rundown','Rust','Scrapyard','Skidrow','Sub Base','Terminal','Underpass','Wasteland']
dlc1maps = ['Bailout','Absturz','Verwuchert','Salvage','Storm']
dlc2maps = ['Carnival','Fuel','Strike','Trailer Park','Vacant']

@client.event
async def on_ready():
    for guild in client.guilds:
        break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}'
    )

@client.event
async def on_message(message):
    # Check that the message is not written by the bot itself
    if message.author == client.user:
        return
    # Check the message for the keyword
    match message.content:
        case '!mw2':
            await message.channel.send('The next Map is ' + getMap())
        case '!mw2dlc1':
            await message.channel.send('The next Map is ' + getDLC1Map())
        case '!mw2dlc2':
            await message.channel.send('The next Map is ' + getDLC2Map())
        case '!mw2og':
            await message.channel.send('The next Map is ' + getOGMap())

def getMap():
    return random.choice(ogmaps + dlc1maps + dlc2maps)

def getDLC1Map():
    return random.choice(ogmaps + dlc1maps)

def getDLC2Map():
    return random.choice(ogmaps + dlc2maps)

def getOGMap():
    return random.choice(ogmaps)

client.run(TOKEN)