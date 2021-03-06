from telethon import TelegramClient
import yaml
import asyncio

async def start(config):
    client = TelegramClient(config["session_name"], config["api_id"], config["api_hash"])
    await client.start()
    print('OUTPUT CHANNEL ID:')
    print('TELEHUNT:')
    print(str((await client.get_entity('https://t.me/telehunt_video')).id))
    print('RYAN_TEST_CHANNEL:')
    print(str((await client.get_entity('https://t.me/ryan_test_channel')).id))
    await client.disconnect()

if __name__ == "__main__":
    with open('config.yml', 'rb') as f:
        config = yaml.safe_load(f)
    
    asyncio.run(start(config))