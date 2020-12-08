import discord
import time
import asyncio
import re
import random

from keep_alive import keep_alive

intents = discord.Intents(messages=True, guilds=True, members=True)

from settings import *

messages = joined = 0

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in...')
    print('Username: ' + str(client.user.name))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='SCAM 1992'))

async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n")

            messages = 0
            joined = 0

            await asyncio.sleep(5)
        except Exception as e:
            print(e)
            await asyncio.sleep(5)

@client.event
async def on_member_join(member):
    global joined
    joined += 1
    for channel in member.server.channels:
        if str(channel) == "welcome":
            await channel.send(f"""Welcome to the server {member.mention}""")


@client.event
async def on_message(message):
    global messages

    messages += 1
    id = client.get_guild(784161461244395570)
    channels = ["commands"]
    valid_users = ["TUDU#4367", "TuDu#5206"]
    bad_words = ["bad", "stop", "dog"]

#message filter
    if(message.author.id != client.user.id):
        for word in bad_words:
            if message.content.count(word) > 0:
                username = message.author.name
                userID = message.author.id
                print("%s has used the Bad Word." % (username))
                await message.channel.purge(limit=1)
                embed = discord.Embed(
                description=" <@%s> don't use banned words." % (userID),
                color=0x00FF00
            )
                await message.channel.send(content=None, embed=embed)
            
#help            
    if message.content == "help":
        embed = discord.Embed(title="BOT Help", description="Commands")
        embed.add_field(name="hello", value="Greets the user")
        embed.add_field(name="!users", value="Prints number of users")
        embed.add_field(name="!shutdown", value="Shut Down the Bot")
        await message.channel.send(content=None, embed=embed)

#hello
    if message.content.find("hello") != -1:
            await message.channel.send("Hi there!") 

#shutdown
    if str(message.channel) in channels and str(message.author) in valid_users:
        if message.content.find("!shutdown") != -1:
            embed = discord.Embed(
                description="Shutting down. Bye! :wave:",
                color=0x00FF00
            )
            await message.channel.send(content=None, embed=embed)
            await client.logout()
            await client.close()
        if message.content == "!users":
            await message.channel.send(f"""Numbers of Members: {id.member_count}""")


keep_alive()
client.loop.create_task(update_stats())
client.run(token) 