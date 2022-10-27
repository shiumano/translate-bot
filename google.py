import discord
import os
import requests
from dotenv import load_dotenv
from googletrans import Translator
load_dotenv()

Token = os.getenv('Token')
source = int(os.getenv('source_channel'))
target = int(os.getenv('target_channel'))
intents = discord.Intents.all() 
client = discord.Client(intents=intents)
translator = Translator()

@client.event
async def on_ready():
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
        if message.channel == source_channel:
            webhooks = await target_channel.webhooks()
            webhook = webhooks[0]
            request = requests.get(f"https://script.google.com/macros/s/AKfycbzowZjdWrs8td1cnJNwjmaVuSmpfR6gpYYQHNnJ6cPHDVedJXtv1K65CWtlZZ0SSgBGHQ/exec?text={message.content}&source=ja&target=en")
            result = request.json()
        elif message.channel == target_channel:
            webhooks = await source_channel.webhooks()
            webhook = webhooks[0]
            request = requests.get(f"https://script.google.com/macros/s/AKfycbzowZjdWrs8td1cnJNwjmaVuSmpfR6gpYYQHNnJ6cPHDVedJXtv1K65CWtlZZ0SSgBGHQ/exec?text={message.content}&source=en&target=ja")
            result = request.json()
        if message.attachments:
            for attachment in message.attachments:
                await webhook.send(content=result["text"]+ "\n" + attachment.url,
                            username=message.author.name,
                            avatar_url=message.author.avatar.url
                            )
        else:
            await webhook.send(content=result["text"],
                            username=message.author.name,
                            avatar_url=message.author.avatar.url
                            )

client.run(Token)