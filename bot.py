# bot.py
import os
import discord
import random
from dotenv import load_dotenv

# Authorization on Server
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Permissions on Server
intents = discord.Intents.default()
intents.message_content = True
intents.typing = True


# Mappools
ogmaps = ['Afghan','Derail','Estate','Favela','Highrise','Invasion','Karachi','Quarry','Rundown','Rust','Scrapyard','Skidrow','Sub Base','Terminal','Underpass','Wasteland']
dlc1maps = ['Bailout','Absturz','Verwuchert','Salvage','Storm']
dlc2maps = ['Carnival','Fuel','Strike','Trailer Park','Vacant']

class CustomClient(discord.Client):
    revoked = []
    vetos = []
    mode = ''
    
    # log when connected
    async def on_ready(self):
        for guild in client.guilds:
            break
        print(
            f'{client.user} is connected to server {guild.name}'
        )
    # respond to messages
    async def on_message(self, message):
        # Check that the message is not written by the bot itself
        if message.author == client.user:
            return
        # Get Admin Role
        adminRole = discord.utils.find(lambda r: r.name == 'MW2 Bot Admin', message.guild.roles)
        # Check the message for the keyword
        match message.content:
            case '!mw2':
                self.mode = 'full'
                await message.channel.send('The next Map is ' + self.getMap())
                self.vetos = []
            case '!mw2dlc1':
                self.mode = 'dlc1'
                await message.channel.send('The next Map is ' + self.getMap())
                self.vetos = []
            case '!mw2dlc2':
                self.mode = 'dlc2'
                await message.channel.send('The next Map is ' + self.getMap())
                self.vetos = []
            case '!mw2og':
                self.mode = 'og'
                await message.channel.send('The next Map is ' + self.getMap())
                self.vetos = []
            case _ if message.content.startswith('!revokeveto'):
                if adminRole in message.author.roles:
                    if not message.mentions:
                        await message.channel.send('No User mentioned! Try tagging them with "@"!')
                    else:
                        for user in message.mentions:
                            await message.channel.send('Revoking veto right for user ' + user.name + '!')
                            if not user.id in self.revoked:
                                self.revoked.append(user.id)
                else:
                    await message.channel.send('You do not have the MW2 Admin Role!')
            case _ if message.content.startswith('!grantveto'):
                if adminRole in message.author.roles:
                    if not message.mentions:
                        await message.channel.send('No User mentioned! Try tagging them with "@"!')
                    else:
                        for user in message.mentions:
                            await message.channel.send('Granting veto right for user ' + user.name + '!')
                            if user.id in self.revoked:
                                self.revoked.remove(user.id)
                else:
                    await message.channel.send('You do not have the MW2 Admin Role!')
            case '!veto':
                #self.vetos.append(126002959250227201)
                if self.mode == '':
                    await message.channel.send('No Mappool has been selected yet!')
                else:
                    #if message.author.id == '126002959250227201':
                    #    await message.channel.send('test')
                    if message.author.id in self.revoked:
                        await message.channel.send(message.author.name + ' was too late today, and has been revoked the right to veto!')
                    elif message.author.id in self.vetos:
                        await message.channel.send(message.author.name + ' has already used their veto!')
                    else:
                        self.vetos.append(message.author.id)
                        await message.channel.send(message.author.name + ' used their veto. The next map is ' + self.getMap())
            case '!mw2help':
                await message.channel.send('Use !mw2 for all maps, !mw2og for non-dlc maps and !mw2dlc1 or !mw2dlc2 for specific dlcs!')
                await message.channel.send('Use !veto to veto a map. You can do this once per mapvoting.')
                await message.channel.send('Users with the "MW2 Bot Admin" Role can also use !revokeveto and !grantveto manage the veto right.')
    # Chooses a random map depending on the mappool
    def getMap(self):
        match self.mode:
            case 'full': 
                return random.choice(ogmaps + dlc1maps + dlc2maps)
            case 'dlc1': 
                return random.choice(ogmaps + dlc1maps)
            case 'dlc2': 
                return random.choice(ogmaps + dlc2maps)
            case 'og': 
                return random.choice(ogmaps)

# Run the Client    
client = CustomClient(intents=intents)
client.run(TOKEN)