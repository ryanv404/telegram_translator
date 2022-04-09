from telethon import TelegramClient, events
from telethon.tl.types import InputChannel
from googletrans import Translator
from switches import get_chat_name, get_flag
import logging
import yaml
import html
import re

# Logging as per docs
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)
logging.getLogger('telethon').setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Set config values
with open('config.yml', 'rb') as f:
    config = yaml.safe_load(f)

# Create the client
client = TelegramClient(config["session_name"], config["api_id"], config["api_hash"])

# Connect client
client.start()
print('[Telethon] Client is listening...')

# Create a translator instance
translator = Translator()

# Get input and output entities for video listener
input_channels_entities = []
output_channel_entities = []

for d in client.iter_dialogs():
    if d.name in config["input_channel_names"] or d.entity.id in config["input_channel_ids"]:
        input_channels_entities.append(InputChannel(d.entity.id, d.entity.access_hash))
    if d.name in config["output_channel_names"] or d.entity.id in config["output_channel_ids"]:
        output_channel_entities.append(InputChannel(d.entity.id, d.entity.access_hash))
        
if not output_channel_entities:
    logger.error(f"Could not find any output channels in the user's dialogs")
    # sys.exit(1)

if not input_channels_entities:
    logger.error(f"Could not find any input channels in the user's dialogs")
    # sys.exit(1)

num_input_channels = len(input_channels_entities)
print(f"[Telethon] Listening to {num_input_channels} {'channel' if num_input_channels == 1 else 'channels'}. Forwarding messages to 2 channels...")

# Listen for new messages
@client.on(events.NewMessage)
async def handler(e):
    # Translate with Google Translator (source language is auto-detected; output language is English)
    content = translator.translate(e.message.message)

    if content.text:
        translation = content.text
        chat = await e.get_chat()
        chat_name = get_chat_name(chat)
        if chat.username:
            link = f't.me/{chat.username}'
        else:
            link = f't.me/c/{chat.id}'

        # Translator mistranslates 'Тривога!' as 'Anxiety' (in this context); change to 'Alert!'
        translated_msg = translation.replace('Anxiety!', 'Alert!')
        
        # Escape input text since using html parsing
        message_id = e.id
        flag = get_flag(content.src)
        border = '~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~'
        message = (
            f'<p><p>{border}\n'
            f'<b>{html.escape(chat_name)}</b>\n'
            f'{border}\n\n</p>'
            f'<p>[TRANSLATED MESSAGE]\n'
            f'{html.escape(translated_msg)}\n\n</p>'
            f'<p>{border}\n'
            f'ORIGINAL LANGUAGE: {flag}\n'
            f'{link}/{message_id} ↩</p></p>') 

        # Message length limit is 4,096 characters; must trim longer messages or they cannot be sent
        if len(message) >= 4096:
            formatting_chars_len = len(
                f'<p><p>{border}\n' + 
                f'<b></b>\n' + 
                f'{border}\n\n</p>' + 
                f'<p>[TRANSLATED MESSAGE]\n' + 
                f'\n\n</p>' + 
                f'<p>{border}\n' + 
                f'ORIGINAL LANGUAGE: {flag}\n' + 
                f'/ ↩</p></p>')
            
            # Subtract 3 for ellipsis; set max length to 4050 as buffer
            desired_msg_len = 4050 - (formatting_chars_len + len(link) + len(str(message_id)) + len(html.escape(chat_name))) - 3
            translated_msg = f'{translated_msg[0:desired_msg_len]}...'
            message = (
                f'<p><p>{border}\n'
                f'<b>{html.escape(chat_name)}</b>\n'
                f'{border}\n\n</p>'
                f'<p>[TRANSLATED MESSAGE]\n'
                f'{html.escape(translated_msg)}\n\n</p>'
                f'<p>{border}\n'
                f'ORIGINAL LANGUAGE: {flag}\n'
                f'{link}/{message_id} ↩</p></p>') 


        if chat.username not in ['shadedPineapple', 'ryan_test_channel', 'UkrRusWarNews', 'telehunt_video', 'cyberbenb', 'Telegram']:
            try:
                await client.send_message(config['aggregator_channel'], message, link_preview=False, parse_mode='html')
            except Exception as exc:
                print('[Telethon] Error while sending message!')
                print(exc)

# Listen for new video messages
@client.on(events.NewMessage(chats=input_channels_entities, func=lambda e: hasattr(e.media, 'document')))
async def handler(e):
    video = e.message.media.document
    if hasattr(video, 'mime_type') and bool(re.search('video', video.mime_type)):
        content = translator.translate(e.message.message)
        if content.text:
            text = content.text
            chat = await e.get_chat()

            if chat.username:
                link = f't.me/{chat.username}'
            else:
                link = f't.me/c/{chat.id}'
            
            message_id = e.id

            # Message length limit is 4,096 characters
            untranslated_msg = e.message.message
            
            # Escape input text since using html parsing
            border = '~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~'
            message = (
                f'<p><p>{link}/{message_id} ↩\n\n'
                f'{border}\n'
                f'<p><b>{chat.title}</b>\n</p>'
                f'{border}\n\n</p>'
                f'<p>[ORIGINAL MESSAGE]\n'
                f'{html.escape(e.message.message)}\n\n</p>'
                f'<p>[TRANSLATED MESSAGE]\n'
                f'{html.escape(text)}</p></p>')
            
            if chat.username not in ['shadedPineapple', 'ryan_test_channel', 'ryan_v404', 'UkrRusWarNews', 'telehunt_video', 'cyberbenb', 'Telegram']:
                try:
                    await client.send_message(output_channel_entities[0], message, parse_mode='html', file=e.media, link_preview=False)
                except Exception as exc:
                    print('[Telethon] Error while forwarding video message!')
                    print(exc)

# Run client until a keyboard interrupt (ctrl+C)
client.run_until_disconnected()