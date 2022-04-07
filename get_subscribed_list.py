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
    dialog_list = []
    async for dialog in client.iter_dialogs():
        dialog_list.append(dialog.entity.username)
    print('FINISHED!')
    print(f'{len(dialog_list)} total dialogs')
    for d in dialog_list:
        print('-', d)
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(start())