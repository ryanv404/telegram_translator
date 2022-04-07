from telethon import TelegramClient, events
from googletrans import Translator
from switches import get_chat_name, get_flag
import logging
import os

# Logging as per docs
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)
logging.getLogger('telethon').setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Set config values
api_id = os.environ.get('api_id')
api_hash = os.environ.get('api_hash')
phone = os.environ.get('phone')
username = os.environ.get('username')
channel_link = os.environ.get('channel_link')

# Create the client
client = TelegramClient(username, api_id, api_hash)

# Connect client
client.start()
print('[Telethon] Client is listening...')

# Create a translator instance
translator = Translator()

# Listen for new messages
@client.on(events.NewMessage)
async def handler(e):
    # Translate with Google Translator (source language is auto-detected; output language is English)
    content = translator.translate(e.message.message)

    if content.text:
        text = content.text
        chat = await e.get_chat()
        chat_name = get_chat_name(chat)

        if chat.username:
            link = f't.me/{chat.username}'
        else:
            link = f't.me/c/{chat.id}'

        # Translator mistranslates 'Тривога!' as 'Anxiety' (in this context); change to 'Alert!'
        text = text.replace('Anxiety!', 'Alert!')
        
        message_id = e.id
        flag = get_flag(content.src)
        message = f'📣\n\n\"{flag}" [{chat_name}]({link})\n\n{text}\n\n[👁‍🗨]({link}/{message_id})'

        if chat.username not in ['ryan_test_channel', 'ryan_v404', 'UkrRusWarNews', 'telehunt_video', 'cyberbenb', 'Telegram']:
            try:
                await client.send_message(channel_link, message, link_preview=False)
            except:
                print('[Telethon] Error while sending message!')

# Run client until a keyboard interrupt (ctrl+C)
client.run_until_disconnected()