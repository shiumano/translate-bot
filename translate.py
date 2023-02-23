from urllib.parse import quote
from dotenv import load_dotenv
load_dotenv()

DeepLToken = os.getenv('DeepLToken')
GoogleAPIUrl = os.getenv('GoogleAPIUrl')

async def deepl(content, source, target, session):
    text = quote(content)
    response = await session.get(f"https://api-free.deepl.com/v2/translate?auth_key={DeepLToken}&text={text}&target_lang=EN")
    result = await response.json()
    return result["translations"][0]["text"]

async def google(content, source, target, session)
    text = quote(content)
    response = await session.get(f"https://script.google.com/{GoogleAPIUrl}/macros/exec?text={text}&source={source}&target={target}")
    result = await response.json()
    return result['text']
