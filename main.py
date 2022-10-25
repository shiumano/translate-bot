import discord
import os
import requests
import datetime
from dotenv import load_dotenv
from discord import app_commands
from discord.app_commands import Choice
load_dotenv()

Token = os.getenv('Token')
source = int(os.getenv('source_channel'))
target = int(os.getenv('target_channel'))
DeepLToken = os.getenv('DeepLToken')
intents = discord.Intents.all() 
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    global source_channel
    global target_channel
    source_channel = client.get_channel(source)
    target_channel = client.get_channel(target)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    elif message.author.discriminator == "0000":
        return
    else:
        try:
            if message.channel == source_channel:
                request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={message.content}&target_lang=EN")
                result = request.json()
                webhooks = await target_channel.webhooks()
                webhook = webhooks[0]
                await webhook.send(content=result["translations"][0]["text"],
                            username=message.author.name,
                            avatar_url=message.author.avatar.url
                            )
            elif message.channel == target_channel:
                request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={message.content}&target_lang=JA")
                result = request.json()
                webhooks = await source_channel.webhooks()
                webhook = webhooks[0]
                await webhook.send(content=result["translations"][0]["text"],
                            username=message.author.name,
                            avatar_url=message.author.avatar.url
                            )
        except Exception:
            if message.channel == source_channel:
                request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={message.content}&target_lang=EN")
                result = request.json()
                webhooks = await target_channel.webhooks()
                webhook = webhooks[0]
                await webhook.send(content=result["translations"][0]["text"],
                            username=message.author.name,
                            avatar_url=message.author.avatar.url
                            )
            elif message.channel == target_channel:
                request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={message.content}&target_lang=JA")
                result = request.json()
                webhook = source_channel.create_webhook(name="日本語")
                await webhook.send(content=result["translations"][0]["text"],
                            username=message.author.name,
                            avatar_url=message.author.avatar.url
                            )

client.run(Token)