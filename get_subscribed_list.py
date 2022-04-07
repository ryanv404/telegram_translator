from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
import asyncio
import os
import yaml
import time
import sys

# Set config values
api_id = os.environ.get('api_id')
api_hash = os.environ.get('api_hash')
phone = os.environ.get('phone')
username = os.environ.get('username')
channel_link = os.environ.get('channel_link')

# Create the client
async def start():
    with open('channel_names.yml', 'rb') as f:
        channel_names = yaml.safe_load(f)
        channel_names = channel_names['channel_names']

    client = TelegramClient(username, api_id, api_hash)
    await client.start()

    print('STARTING...')
    dialog_list = []
    async for dialog in client.iter_dialogs():
        if dialog.entity.username is not None:
            dialog_list.append(dialog.entity.username)

    for channel_name in channel_names[0:5]:
        try:
            await client(JoinChannelRequest(channel_name))
            print('SUBSCRIBED TO', channel_name)
            time.sleep(5)
        except Exception as e:
            print('COULD NOT SUBSCRIBE TO', channel_name)
            print(e)
            sys.exit(1)

    print('FINISHED!')
    print(f'{len(list(set([*dialog_list, *channel_names])))} total dialogs')

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(start())