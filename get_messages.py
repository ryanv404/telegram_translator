# t.me/opersvodki/3054
# for some reason a link to t.me/opersvodki/3051 was inserted at the '4'

from telethon import TelegramClient, sync
from telethon.tl.functions.messages import GetHistoryRequest
from googletrans import Translator
import yaml

with open('config.yml', 'rb') as f:
    config = yaml.safe_load(f)

# Create the client
client = TelegramClient(config["session_name"], config["api_id"], config["api_hash"])

# Connect client
client.start()

# Create a translator instance
translator = Translator()

# Get messages
channel_username = 'opersvodki'
channel_entity = client.get_entity(channel_username)

posts = client(GetHistoryRequest(
    peer=channel_entity,
    limit=10,
    offset_date=None,
    offset_id=0,
    max_id=0,
    min_id=0,
    add_offset=0,
    hash=0))

# Messages stored in `posts.messages`
message_num = 1
for message in posts.messages:
    print(f'MESSAGE NUMBER {message_num}:')
    print(message)
    message_num += 1

# Translate with Google Translator (source language is auto-detected; output language is English)
# content = translator.translate(e.message.message)
# text = content.text

# chat = await e.get_chat()
# if chat.username:
#     link = f't.me/{chat.username}'
# else:
#     link = f't.me/c/{chat.id}'

# message_id = e.id
# border = '~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~'
# message = f'{link}/{message_id} ↩\n\n{border}\n{chat.title}\n{border}\n\n[ORIGINAL MESSAGE]\n{e.message.message}\n\n[TRANSLATED MESSAGE]\n{text}'

# Run client until a keyboard interrupt (ctrl+C)
client.run_until_disconnected()