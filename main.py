import discord
import os
import requests
import langid
from discord import app_commands
from dotenv import load_dotenv

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
    global source_channel
    global target_channel
    source_channel = client.get_channel(source)
    target_channel = client.get_channel(target)
    await tree.sync()


@client.event
async def on_message(message):
    if message.author.bot or message.author.discriminator == "0000":
        return
    else:
        if message.channel == source_channel:
            try:
                webhooks = await target_channel.webhooks()
                webhook = webhooks[0]
            except IndexError:
                webhook = await target_channel.create_webhook(name="英語")
            r = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={message.content}&target_lang=EN")
            result = r.json()
        elif message.channel == target_channel:
            try:
                webhooks = await source_channel.webhooks()
                webhook = webhooks[0]
            except IndexError:
                webhook = await source_channel.create_webhook(name="日本語")
            r = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={message.content}&target_lang=JA")
            result = r.json()
        if message.attachments:
            for attachment in message.attachments:
                await webhook.send(content=result["translations"][0]["text"] + "\n" + attachment.url,
                                   username=message.author.display_name,
                                   avatar_url=message.author.display_avatar.url
                                   )
        else:
            await webhook.send(content=result["translations"][0]["text"],
                               username=message.author.display_name,
                               avatar_url=message.author.display_avatar.url
                               )


@tree.context_menu(name="Translate Message")
async def translate(interaction: discord.Interaction, message: discord.Message):
    details = langid.classify(message.content)
    if "en" == details[0]:
        r = requests.get(
            f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={message.content}&target_lang=JA")
        result = r.json()
    elif "ja" == details[0]:
        r = requests.get(
            f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={message.content}&target_lang=EN")
        result = r.json()
    else:
        await interaction.response.send_message("Error", ephemeral=True)
    await interaction.response.send_message(result["translations"][0]["text"], ephemeral=True)

client.run(Token)
