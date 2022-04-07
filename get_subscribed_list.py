from telethon import TelegramClient
import asyncio
import os

# Set config values
api_id = os.environ.get('api_id')
api_hash = os.environ.get('api_hash')
phone = os.environ.get('phone')
username = os.environ.get('username')
channel_link = os.environ.get('channel_link')

# Create the client

async def start():
    client = TelegramClient(username, api_id, api_hash)
    await client.start()

    print('STARTING...')
    print('dialogs list:')
    num = 1
    for dialog in client.iter_dialogs():
        print(f'DIALOG #{num}')
        print(dialog)
        num += 1
    print('FINISHED!')
    client.disconnect()

if __name__ == "__main__":
    asyncio.run(start())