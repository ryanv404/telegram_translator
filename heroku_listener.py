import os
import logging
from googletrans import Translator
from telethon import TelegramClient, events

# Logging as per docs
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# Create a translator instance
translator = Translator()

# Set config values
api_id = os.environ.get('api_id')
api_hash = os.environ.get('api_hash')
phone = os.environ.get('phone')
username = os.environ.get('username')
channel_link = os.environ.get('channel_link')

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
            return 'TASS \nRussia state-affiliated media 🤨'
        case 'MID_Russia':
            return 'MID Russia \nRussia state-affiliated media 🤨'
        case 'rian_ru':
            return 'RIA Novosti \nRussia state-affiliated media 🤨'
        case 'mvs_ukraine':
            return 'MVS Ukraine \nUkraine state-affiliated media 🤷‍♂️'
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
        case 'a_shtirlitz':
            return 'Anatoly Shtirlitz'
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

        if chat.username:
            link = f't.me/{chat.username}'
        else:
            link = f't.me/c/{chat.id}'

        flag = get_flag(content.src)
        message_id = e.id
        message = f'📣 \n\n\"{flag}" [{chat_name}]({link}) \n\n{content.text} \n\n[👁‍🗨]({link}/{message_id})'

        try:
            await client.send_message(channel_link, message, link_preview=False)
        except:
            print('[Telethon] Error while sending message!')

# Connect client
client.start()
print('[Telethon] Client is listening...')

# Run client until a keyboard interrupt (ctrl+C)
client.run_until_disconnected()