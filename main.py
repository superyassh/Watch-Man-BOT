import discord
import time
import asyncio
from googleapiclient import discovery
import json
import aiohttp
import random
import secrets

from keep_alive import keep_alive
intents = discord.Intents.default()
intents.members=True
client = discord.Client(intents=intents)
intents = discord.Intents(messages=True, guilds=True, members=True)


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
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name='Over You'))


async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(
                    f"Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n"
                )

            messages = 0
            joined = 0

            await asyncio.sleep(5)
        except Exception as e:
            print(e)
            await asyncio.sleep(5)


@client.event
async def on_message_join(member):
    channel = client.get_channel(channel_id)
    embed=discord.Embed(title=f"Welcome {member.name}", description=f"Thanks for joining {member.guild.name}!") # F-Strings!
    embed.set_thumbnail(url=member.avatar_url) # Set the embed's thumbnail to the member's avatar image!
    await channel.send(embed=embed)


@client.event
async def on_message(message):
    global messages

    messages += 1
    id = client.get_guild(784161461244395570)
    channels = ["commands"]
    valid_users = ["TUDU#4367", "TuDu#5206", "0xKage#5206"]

    if (message.author.id != client.user.id):
        API_KEY = 'AIzaSyCq17LT42MhHnGO0MIwSymviKVz3m9vFMI'
        clientGoogle = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=API_KEY,
            discoveryServiceUrl=
            "https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
            static_discovery=False,
        )
        analyze_request = {
            'comment': {
                'text': message.content
            },
            'requestedAttributes': {
                'TOXICITY': {}
            }
        }
        response = clientGoogle.comments().analyze(
            body=analyze_request).execute()
        # response_dict=json.loads(response.content)
        results = json.dumps(response, indent=2)
        json_results = json.loads(results)
        toxicity = json_results['attributeScores']['TOXICITY']['summaryScore'][
            'value']
        #print(json.dumps(response,indent=2))
        #print(toxicity)
        toxicity_percentage = toxicity*100
        if toxicity > 0.9:
            username = message.author.name
            userID = message.author.id
            print("%s has used the Bad Word which has toxicity is %s" %
                  (username, toxicity))
            await message.channel.purge(limit=1)
            embed = discord.Embed(
                description=
                " <@%s> don't use banned words.\n\n Toxicity in your Message is %.2f %%"
                % (userID, toxicity_percentage),
                color=0x00FF00)
            await message.channel.send(content=None, embed=embed)
            await message.author.send(content=None, embed=embed)
            with open("data.txt", "a") as f:
                        f.write(
                            f"%s has used the Bad Word which has toxicity level %s\n"
                            % (username, toxicity))

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

#hello
    if message.content == "!users":
        await message.channel.send(f"""Numbers of Members: {id.member_count}"""
                                   )


#shutdown
    if message.content.find(
            "!shutdown") != -1 and message.author in valid_users:
        embed = discord.Embed(description="Shutting down. Bye! :wave:",
                              color=0x00FF00)
        await message.channel.send(content=None, embed=embed)
        await client.logout()
        await client.close()

    if message.content == "!cats":
        async with aiohttp.ClientSession() as cs:
            async with cs.get('http://aws.random.cat/meow') as r:
                res = await r.json()
                emojis = [':cat2: ', ':cat: ', ':heart_eyes_cat: ']
                await message.channel.send(random.choice(emojis) + res['file'])

    if message.content == "!dogs":
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://dog.ceo/api/breeds/image/random') as r:
                res = await r.json()
                emojis = [':dog: ', ':dog2: ']
                await message.channel.send(random.choice(emojis) + res['message'])
                
    if message.content == "tell me a joke":
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://v2.jokeapi.dev/joke/Any?type=single') as r:
                res = await r.json()
                emojis = [':speech_left:  ']
                await message.channel.send(random.choice(emojis) + res['joke'])

    if message.content == "ip":
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://api.ipgeolocation.io/ipgeo?apiKey=78a1ccc7c8dd40f8ad8973953a3d14e6') as r:
                res = await r.json()
                emojis = [':speech_left:  ']
                await message.channel.send(random.choice(emojis) + res['city'])
                
    if message.content == "!countdown":
        countdown = ['five', 'four', 'three', 'two', 'one']
        for num in countdown:
            await message.channel.send('**:{0}:**'.format(num))
            await asyncio.sleep(1)
        await message.channel.send('**:ok:** BOOM')

    if message.content == "!flipcoin":
        coinsides = ["Heads", "Tails"]
        await message.channel.send(f"**{message.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

    if message.content == "!genpass":
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.passwordrandom.com/query?command=password&format=json&count=1') as r:
                res = await r.json()
                for i in res.values():
                  pass
                emojis = [':key: ', ':key2: ']
                await message.channel.send(f"{random.choice(emojis)}{i}")

keep_alive()
client.loop.create_task(update_stats())
client.run(token)
