import discord
import os
import requests
from dotenv import load_dotenv

load_dotenv()

Token = os.getenv('Token')
source = int(os.getenv('source_channel'))
target = int(os.getenv('target_channel'))
DeepLToken = os.getenv('DeepLToken')
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    global source_channel
    global target_channel
    source_channel = client.get_channel(source)
    target_channel = client.get_channel(target)

@client.event
async def on_message(message):
    if message.author.bot or message.author.discriminator == "0000":
        return
    else:
        if message.channel == source_channel:
            try:
                webhooks = await target_channel.webhooks()
                webhook = webhooks[0]
            except Exception:
                webhook = await target_channel.create_webhook(name="英語")
            r = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={message.content}&target_lang=EN")
            result = r.json()
        elif message.channel == target_channel:
            try:
                webhooks = await source_channel.webhooks()
                webhook = webhooks[0]
            except Exception:
                webhook = await source_channel.create_webhook(name="日本語")
            r = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={message.content}&target_lang=JA")
            result = r.json()
        if message.attachments:
            for attachment in message.attachments:
                await webhook.send(content=result["translations"][0]["text"] + "\n" + attachment.url,
                                   username=message.author.name,
                                   avatar_url=message.author.avatar.url
                                   )
        else:
            await webhook.send(content=result["translations"][0]["text"],
                               username=message.author.name,
                               avatar_url=message.author.avatar.url
                               )

client.run(Token)