import discord
import asyncio
import cakebot_config

client = discord.Client()
invite = 'https://discordapp.com/oauth2/authorize?client_id=178312661233172480&scope=bot&permissions=66186303'

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    content = message.content

    if content.startswith('!hello'):
        await client.send_message(message.channel, 'Hello {}!'.format(message.author.mention))
    elif content.startswith('!'):
        await client.send_message(message.channel, 'Unknown command!')

client.run(cakebot_config.token)
