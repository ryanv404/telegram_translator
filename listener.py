import os
import logging
from switches import get_chat_name, get_flag
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