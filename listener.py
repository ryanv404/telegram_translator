import logging
import configparser
from googletrans import Translator
from telethon import TelegramClient, events

# Logging as per docs
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# Create a translator instance
translator = Translator()

# Read config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# Set config values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
phone = config['Telegram']['phone']
username = config['Telegram']['username']
channel_link = config['Telegram']['channel_link']

# Create the client
client = TelegramClient(username, api_id, api_hash)

# Switch source language to the corresponding flag emoji
def get_flag(src):
    match src:
            case 'en':
                return "🇬🇧"
            case 'uk':
                return "🇺🇦"
            case 'ru':
                return "🇷🇺"
            case _:
                return "🇦🇶"

# Mark state-affiliated media channels and format channel names
def get_chat_name(chat):
    match chat.username:
        case 'tass_agency':
            return 'TASS \n~~Russia state-affiliated media 🤨~~'
        case 'MID_Russia':
            return 'MID Russia \n~~Russia state-affiliated media 🤨~~'
        case 'rian_ru':
            return 'RIA Novosti \n~~Russia state-affiliated media 🤨~~'
        case 'mvs_ukraine':
            return 'MVS Ukraine \n~~Ukraine state-affiliated media 🤷‍♂️~~'
        case 'insiderUKR':
            return 'Insider Ukraine War News'
        case 'uniannet':
            return 'UNIAN - Ukraine News'
        case 'voynareal':
            return 'Real War News Ukraine'
        case 'suspilnesumy':
            return 'Public Sumy'
        case 'milinfolive':
            return 'Military Informant'
        case 'KharkivPolitics':
            return 'Kharkiv.Main.Politics'
        case 'KyivPolitics':
            return 'Kyiv.Main.Politics'
        case 'faceofwar':
            return 'Face of War'
        case 'ukr_pravda':
            return 'Ukraine Pravda'
        case _:
            if chat.title:
                return chat.title
            else:
                return chat.username
                

# Listen for new messages
@client.on(events.NewMessage)
async def handler(e):
    # Translate with Google Translator (source language is auto-detected; output language is English)
    content = translator.translate(e.message.message)

    if content.text:
        chat = await e.get_chat()
        chat_name = get_chat_name(chat)
        print(str(chat.id) + '/' + str(e.id))

        link = f't.me/{chat.username}'
        flag = get_flag(content.src)
        message = f'\"{flag}"  **[{chat_name}]({link})**\n\n{content.text}'

        await client.send_message(channel_link, message, link_preview=False)

# Connect client
client.start()
print('[Telethon] Client is listening...')

# Run client until a keyboard interrupt (ctrl+C)
client.run_until_disconnected()