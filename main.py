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

@tree.command(name="translate")
@app_commands.describe(lang='翻訳先の言語')
@app_commands.describe(text='翻訳したい内容')
@app_commands.choices(lang=[
    Choice(name='日本語', value="ja"),
    Choice(name='英語', value="en"),
    Choice(name='中国語', value="zh"),
    Choice(name='ロシア語', value="ru"),
    Choice(name='ドイツ語', value="de"),
    Choice(name='フランス語', value="fr"),
    Choice(name='イタリア語', value="it"),
    Choice(name='スペイン語', value="es"),
    Choice(name='ブルガリア語', value="bg"),
    Choice(name='チェコ語', value="cs"),
    Choice(name='デンマーク語', value="da"),
    Choice(name='ギリシャ語', value="el"),
    Choice(name='エストニア語', value="et"),
    Choice(name='フィンランド語', value="fl"),
    Choice(name='ハンガリー語', value="hu"),
    Choice(name='インドネシア語', value="id"),
    Choice(name='オランダ語', value="nl"),
    Choice(name='ポーランド語', value="pl"),
    Choice(name='ポルトガル語', value="pt"),
    Choice(name='スウェーデン語', value="sv"),
    Choice(name='トルコ語', value="tr"),
    Choice(name='ウクライナ語', value="uk")
])
async def translate(interaction: discord.Interaction, lang: Choice[str], text: str):
    """翻訳する"""
    await interaction.response.defer(thinking=True)
    if lang.value == "ja":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=JA")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="日本語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
        await interaction.followup.send(embed=embed)
    elif lang.value == "en":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=EN")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="英語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
        await interaction.followup.send(embed=embed)
    elif lang.value == "zh":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=ZH")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="中国語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
        await interaction.followup.send(embed=embed)
    elif lang.value == "ru":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=RU")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="ロシア語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
        await interaction.followup.send(embed=embed)
    elif lang.value == "de":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=DE")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="ドイツ語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
        await interaction.followup.send(embed=embed)
    elif lang.value == "fr":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=FR")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="フランス語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
        await interaction.followup.send(embed=embed)
    elif lang.value == "it":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=IT")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="イタリア語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
        await interaction.followup.send(embed=embed)
    elif lang.value == "es":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=ES")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="スペイン語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
        await interaction.followup.send(embed=embed)
    elif lang.value == "bg":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=BG")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="ブルガリア語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
        await interaction.followup.send(embed=embed)
    elif lang.value == "cs":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=CS")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="チェコ語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
        await interaction.followup.send(embed=embed)
    elif lang.value == "da":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=DA")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="デンマーク語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
        await interaction.followup.send(embed=embed)
    elif lang.value == "el":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=EL")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="ギリシャ語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
        await interaction.followup.send(embed=embed)
    elif lang.value == "et":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=ET")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="エストニア語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
        await interaction.followup.send(embed=embed)
    elif lang.value == "fl":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=FL")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="フィンランド語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
        await interaction.followup.send(embed=embed)
    elif lang.value == "hu":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=HU")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="ハンガリー語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
        await interaction.followup.send(embed=embed)
    elif lang.value == "id":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=ID")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="インドネシア語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
        await interaction.followup.send(embed=embed)
    elif lang.value == "nl":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=NL")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="オランダ語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
        await interaction.followup.send(embed=embed)
    elif lang.value == "pl":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=PL")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="ポーランド語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
        await interaction.followup.send(embed=embed)
    elif lang.value == "pt":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=PT")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="ポルトガル語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
    elif lang.value == "sv":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=SV")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="スウェーデン語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
        await interaction.followup.send(embed=embed)
    elif lang.value == "tr":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=TR")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="トルコ語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
        await interaction.followup.send(embed=embed)
    elif lang.value == "uk":
        request = requests.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=UK")
        result = request.json()
        embed = discord.Embed(title="翻訳結果",color=0x00ff00,timestamp=datetime.now())
        embed.add_field(name="原文",value=text)
        embed.add_field(name="ウクライナ語",value=result["translations"][0]["text"])
        embed.set_footer(text="Translated by DeepL")
        await interaction.followup.send(embed=embed)
    else:
        embed = discord.Embed(title="エラー", description="その言語には翻訳できません\n別の言語を選んでください", color=0xff0000)
        await interaction.followup.send(embed=embed, ephemeral=True)

client.run(Token)