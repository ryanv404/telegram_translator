from telethon import TelegramClient
import asyncio
import os
import yaml

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

    print('CHANNELS LIST:')
    dialog_list = []
    async for dialog in client.iter_dialogs():
        if dialog.entity.username is not None:
            dialog_list.append(dialog.entity.username)
            print('-', dialog.entity.username)

    print(f'{len(list(set(dialog_list)))} total subscriptions')

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(start())