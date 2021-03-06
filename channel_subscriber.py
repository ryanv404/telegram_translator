from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import errors
import asyncio
import os
import yaml
import time

# Set config values
api_id = os.environ.get('api_id')
api_hash = os.environ.get('api_hash')
phone = os.environ.get('phone')
username = os.environ.get('username')
channel_link = os.environ.get('channel_link')

with open('config.yml', 'rb') as f:
    config = yaml.safe_load(f)
    
# Create the client
async def start():
    with open('channel_names.yml', 'rb') as f:
        channel_names = yaml.safe_load(f)
        channel_names = channel_names['channel_names']

    client = TelegramClient(config["session_name"], config["api_id"], config["api_hash"])
    await client.start()

    print('STARTING...')
    dialog_list = []
    async for dialog in client.iter_dialogs():
        if dialog.entity.username is not None:
            dialog_list.append(dialog.entity.username)

    for channel_name in channel_names:
        if channel_name not in dialog_list:
            try:
                await client(JoinChannelRequest(channel_name))
                print('SUBSCRIBED TO', channel_name)
            except errors.FloodWaitError as e:
                print('COULD NOT SUBSCRIBE TO', channel_name)
                print('Flood wait for', e.seconds, 'seconds')
                time.sleep(e.seconds)
            except Exception as e:
                print('COULD NOT SUBSCRIBE TO', channel_name)
                print(e)

    print('FINISHED!')
    new_dialog_list = []
    async for dialog in client.iter_dialogs():
        if dialog.entity.username is not None:
            print('-', dialog.entity.username)
            new_dialog_list.append(dialog.entity.username)

    print(f'{len(list(set(new_dialog_list)))} total subscriptions')

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(start())