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
    dialogs = await client.iter_dialogs()
    print('dialogs list:')
    print(dialogs)
    print('first 2 dialogs:')
    print(dialogs[0])
    print(dialogs[1])
    print('FINISHED!')
    client.disconnect()

if __name__ == "__main__":
    asyncio.run(start())