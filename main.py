import discord
import sys
import os
import translate
import langid
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

Token = os.getenv('Token')
source = int(os.getenv('source_channel'))
target = int(os.getenv('target_channel'))

if len(sys.argv) == 2:
    if sys.argv[1] == 'deepl':
        print('Use DeepL.')
        tr = translate.deepl
    elif sys.argv[1] == 'google':
        print('Use Google Tanslate')
        tr = translate.google
    else:
        print('Please choise deepl or google')
        sys.exit(1)
else:
    print('please select translator')
    sys.exit(1)


class MyClient(discord.Client):
    @property
    def session(self):
        return self.http._HTTPClient__session

intents = discord.Intents.all()
client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    global source_channel
    global target_channel
    source_channel = client.get_channel(source)
    target_channel = client.get_channel(target)
    await tree.sync()


async def send(channel, message, text):
    webhooks = await channel.webhooks()
    if len(webhooks) == 0:
        webhook = webhooks[0]
    else:
        webhook = await channel.create_webhook(name="Translate")

    await webhook.send(content=text,
                       username=message.author.display_name,
                       avatar_url=message.author.display_avatar.url
                       )

    for attachment in message.attachments:
        await webhook.send(content=attachment.url,
                           username=message.author.display_name,
                           avatar_url=message.author.display_avatar.url
                           )


@client.event
async def on_message(message):
    if message.author.bot or message.author.discriminator == "0000":
        return
    else:
        if message.channel == source_channel:
            await send(
                target_channel,
                message,
                tr(message.content, source="ja", target="en")
            )
        elif message.channel == target_channel:
            await send(
                source_channel,
                message,
                tr(message.content, source="en", target="ja")
            )


@tree.context_menu(name="Translate Message")
async def translate(interaction: discord.Interaction, message: discord.Message):
    details = langid.classify(message.content)
    text = message.content.replace("#", "<sharp>")
    if "en" == details[0]:
        await interaction.response.send_message(tr(message.content, source="en", target="ja").replace("<sharp>", "#"), ephemeral=True)
    elif "ja" == details[0]:
        await interaction.response.send_message(tr(message.content, source="ja", target="en").replace("<sharp>", "#"), ephemeral=True)
    else:
        await interaction.response.send_message("Error", ephemeral=True)


client.run(Token)
