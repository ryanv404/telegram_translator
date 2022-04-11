from telethon import TelegramClient, events
from telethon.tl.types import InputChannel
from googletrans import Translator
from switches import get_chat_name
from filter_results import eng_search_terms_present, ru_search_terms_present
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
    logger.error(f"[Telethon] Could not find any output channels in the user's dialogs")
if not input_channels_entities:
    logger.error(f"[Telethon] Could not find any input channels in the user's dialogs")

num_input_channels = len(input_channels_entities)
num_output_channels = len(output_channel_entities)
print(f"[Telethon] Listening to {num_input_channels} {'channel' if num_input_channels == 1 else 'channels'}. Forwarding messages to {num_output_channels} {'channel' if num_output_channels == 1 else 'channels'}...")

# Output channels
war_news_channel = config['output_channel_ids'][0]
video_channel = config['output_channel_ids'][1]
search_channel = config['output_channel_ids'][2]
photo_channel = config['output_channel_ids'][3]

# Listen for new messages
@client.on(events.NewMessage)
async def handler(e):
    # Translate with Google Translator (source language is auto-detected; output language is English)
    content = translator.translate(e.message.message)
    if content.text:
        translation = content.text
    else:
        translation = ''

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
    border = '~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~'
    message = (
        f'<p><p>{border}\n'
        f'<b>{html.escape(chat_name)}</b>\n'
        f'{border}\n\n</p>'
        f'<p>[TRANSLATED MESSAGE]\n'
        f'{html.escape(translated_msg)}\n\n</p>'
        f'<p>{border}\n'
        f'{link}/{message_id} ↩</p></p>') 

    # Message length limit appears to be around 3980 characters; must trim longer messages or they cannot be sent
    if len(message) >= 3980:
        formatting_chars_len = len(
            f'<p><p>{border}\n' + 
            f'<b>{html.escape(chat_name)}</b>\n' + 
            f'{border}\n\n</p>' + 
            f'<p>[TRANSLATED MESSAGE]\n' + 
            f'\n\n</p>' + 
            f'<p>{border}\n' + 
            f'{link}/{message_id} ↩</p></p>')
        
        # Subtract 3 for ellipsis
        desired_msg_len = 3980 - formatting_chars_len - 3
        translated_msg = f'{translated_msg[0:desired_msg_len]}...'
        message = (
            f'<p><p>{border}\n'
            f'<b>{html.escape(chat_name)}</b>\n'
            f'{border}\n\n</p>'
            f'<p>[TRANSLATED MESSAGE]\n'
            f'{html.escape(translated_msg)}\n\n</p>'
            f'<p>{border}\n'
            f'{link}/{message_id} ↩</p></p>') 

    if chat.username not in ['photo_posts', 'shadedPineapple', 'my_search_results', 'video_posts', 'ukr_rus_war_news', 'cyberbenb', 'Telegram']:
        if eng_search_terms_present(translated_msg) or ru_search_terms_present(e.message.message): 
            try:
                await client.send_message(search_channel, message, link_preview=False, parse_mode='html')
            except Exception as exc:
                print('[Telethon] Error while sending fc message!')
                print(exc)
        
        try:
            await client.send_message(war_news_channel, message, link_preview=False, parse_mode='html')
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
            translation = content.text
        else:
            translation = ''
        
        chat = await e.get_chat()

        if chat.username:
            link = f't.me/{chat.username}'
        else:
            link = f't.me/c/{chat.id}'
        
        message_id = e.id

        # Escape input text since using html parsing
        untranslated_msg = e.message.message
        border = '~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~'
        message = (
            f'<p><p>{link}/{message_id} ↩\n\n'
            f'{border}\n'
            f'<p><b>{chat.title}</b>\n</p>'
            f'{border}\n\n</p>'
            f'<p>[ORIGINAL MESSAGE]\n'
            f'{html.escape(untranslated_msg)}\n\n</p>'
            f'<p>[TRANSLATED MESSAGE]\n'
            f'{html.escape(translation)}</p></p>')

        # Video message length limit appears to be around 1024 characters; must trim longer messages or they cannot be sent
        if len(message) >= 1024:
            formatting_chars_len = len(
                f'<p><p>{link}/{message_id} ↩\n\n'
                f'{border}\n'
                f'<p><b>{chat.title}</b>\n</p>'
                f'{border}\n\n</p>'
                f'<p>[ORIGINAL MESSAGE]\n'
                f'\n\n</p>'
                f'<p>[TRANSLATED MESSAGE]\n'
                f'</p></p>')
            
            # Subtract 6 for ellipses; 
            desired_msg_len = (1024 - formatting_chars_len - 6) // 2
            translated_msg = f'{translation[0:desired_msg_len]}...'
            untranslated_msg = f'{untranslated_msg[0:desired_msg_len]}...'
            message = (
                f'<p><p>{link}/{message_id} ↩\n\n'
                f'{border}\n'
                f'<p><b>{chat.title}</b>\n</p>'
                f'{border}\n\n</p>'
                f'<p>[ORIGINAL MESSAGE]\n'
                f'{html.escape(untranslated_msg)}\n\n</p>'
                f'<p>[TRANSLATED MESSAGE]\n'
                f'{html.escape(translated_msg)}</p></p>')
            
        try:
            await client.send_message(video_channel, message, parse_mode='html', file=e.media, link_preview=False)
        except Exception as exc:
            print('[Telethon] Error while forwarding video message!')
            print(exc)
            print(e.message)

# Listen for new photo messages
@client.on(events.NewMessage(chats=input_channels_entities, func=lambda e: hasattr(e.media, 'photo')))
async def handler(e):
    chat = await e.get_chat()
    if chat.username:
        link = f't.me/{chat.username}'
    else:
        link = f't.me/c/{chat.id}'
    
    message_id = e.id

    border = '~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~'
    message = (
        f'<p>{link}/{message_id} ↩\n\n'
        f'{border}\n</p>'
        f'<b>{chat.title}</b>\n'
        f'{border}\n\n</p>')

    try:
        await client.send_message(photo_channel, message, parse_mode='html', file=e.media, link_preview=False)
    except Exception as exc:
        print('[Telethon] Error while forwarding video message!')
        print(exc)
        print(e.message)

# Run client until a keyboard interrupt (ctrl+C)
client.run_until_disconnected()