from telethon import TelegramClient
import asyncio
import yaml

# Create the client
async def start():
    # Set config values
    with open('config.yml', 'rb') as f:
        config = yaml.safe_load(f)

    # Create the client
    client = TelegramClient(config["session_name"], config["api_id"], config["api_hash"])

    # Connect client
    await client.start()

    print('CHANNELS LIST:')
    dialog_list = []
    async for dialog in client.iter_dialogs():
        if not dialog.is_group and dialog.is_channel:
            dialog_list.append(dialog.entity.username)
            print('-', dialog.entity.username)

    print(f'{len(list(set(dialog_list)))} total subscriptions')

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(start())