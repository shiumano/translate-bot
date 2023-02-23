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


async def send(channel, message, text):
    try:
        webhooks = await channel.webhooks()
        webhook = webhooks[0]
    except IndexError:
        await channel.create_webhook(name="Translate")
    if message.attachments:
        for attachment in message.attachments:
            await webhook.send(content=text + "\n" + attachment.url,
                               username=message.author.display_name,
                               avatar_url=message.author.display_avatar.url
                               )
    else:
        await webhook.send(content=text,
                           username=message.author.display_name,
                           avatar_url=message.author.display_avatar.url
                           )


def tr(text, source, target):
    r = requests.get(f"https://script.google.com/macros/s/AKfycbzowZjdWrs8td1cnJNwjmaVuSmpfR6gpYYQHNnJ6cPHDVedJXtv1K65CWtlZZ0SSgBGHQ/exec?text={text}&source={source}&target={target}")
    return r.json()['text']


@client.event
async def on_message(message):
    if message.author.bot or message.author.discriminator == "0000":
        return
    else:
        if message.channel == source_channel:
            await send(channel=target_channel, message=message, text=tr(text=message.content, source="ja", target="en"))
        elif message.channel == target_channel:
            await send(channel=source_channel, message=message, text=tr(text=message.content, source="en", target="ja"))


@tree.context_menu(name="Translate Message")
async def translate(interaction: discord.Interaction, message: discord.Message):
    details = langid.classify(message.content)
    if "en" == details[0]:
        await interaction.response.send_message(tr(text=message.content, source="en", target="ja"), ephemeral=True)
    elif "ja" == details[0]:
        await interaction.response.send_message(tr(text=message.content, source="ja", target="en"), ephemeral=True)
    else:
        await interaction.response.send_message("Error", ephemeral=True)

client.run(Token)
