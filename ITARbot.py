# Import libraries
import os
import sys
import json
import discord
import logging
import discord.ext.commands

# War thunder replays
# usr: Aries_B
# pwd: aries_bot
# https://warthunder.com/en/tournament/replay/

# https://discord.com/api/oauth2/authorize?client_id=708655185378934804&permissions=8&scope=bot

# Logger setup
logging.basicConfig(level=logging.INFO)

# Folders
FOLDER = "./Dati/"
if not os.path.isdir(FOLDER):
    os.mkdir(FOLDER)

# Token
FILE_TOKEN = FOLDER+'/token.json'
if os.path.isfile(FILE_TOKEN):
    file = open(file=FILE_TOKEN,mode="r",encoding="utf-8")
    dati_token = json.loads(file.read(),encoding="utf-8")
    file.close()
else:
    sys.exit("No tokenfile, aborting")

TOKEN = dati_token["discord_bot"]

# Command prefix structure
class CMD_Prefix:
    def __call__(self, bot, message):
        return "!"

# Get the bot
bot = discord.ext.commands.Bot(command_prefix=CMD_Prefix, help_command=None)

# Handle ready event
@bot.event
async def on_ready():
    print(str(bot.user)+" has connected to Discord!")

    print("Listing managed guilds:")
    for guild in bot.guilds:
        print("- "+str(guild.name)+" ("+str(guild.id)+")")
        print("\n List of roles in the guild:")
        for role in guild.roles:
            print("  - "+str(role.name)+" ("+str(role.id)+")")
        print("\n")


# Handle joining a server
@bot.event
async def on_guild_join(guild):
    print("Joined guild "+str(guild.name)+" ("+str(guild.id)+")")


# Handle player join
@bot.event
async def on_member_join(member):
    # Log to terminal
    print(str(member.name)+" ("+str(member.id)+") has joined the guild '" +
          str(member.guild.name)+"' ("+str(member.guild.id)+")")
    
    # Greet the member
    await member.create_dm()
    await member.dm_channel.send(
        f'Salve {member.name}, benvenuto nel canale della squadriglia!\n' +
        'Dai un occhio al canale #info-e-reclutamento per più informazioni'
    )


# Handle messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
        # Ignore bot message
        return

    print(str(message.author.name) + " ("+str(message.author.id)+") sent <"+str(message.content)+"> on channel '"+str(message.channel.name) +
          "' ("+str(message.channel.id)+") of guild '"+str(message.channel.guild.name)+"' ("+str(message.channel.guild.id)+")")


# Finally run the bot
bot.run(token)
