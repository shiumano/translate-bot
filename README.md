# translate-bot
Discordで相互の翻訳チャンネルを実装するボット<br>
(例)<br>
英語→日本語<br>
日本語→英語<br>
## 使い方
STep1 .envに次のように記述する<br>
```
Token="DiscordToken" #DiscordBotトークン
source_channel="1035219664780927118" #日本語のチャンネルID
target_channel="1035219699367157842" #英語のチャンネルID
DeepLToken="DeepLAPIKey" #DeepLを使う場合はDeepL APIのキーを記述
GoogleAPIUrl="GoogleAPIKey" #Google翻訳を使う場合はGASのUrlを記述
```
Step2 翻訳サービスを選ぶ<br>
Google翻訳を使う場合 `$ python3 main.py google`<br>
DeepL翻訳を使う場合 `$ python3 main.py deepl`<br>

Enjoy
