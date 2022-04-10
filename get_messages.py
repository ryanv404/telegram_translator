from telethon import TelegramClient, sync
from telethon.tl.functions.messages import GetHistoryRequest
# import asyncio
from telethon.tl import functions, types
import yaml
import re

# Set config values
with open('config.yml', 'rb') as f:
    config = yaml.safe_load(f)

# Create the client
client = TelegramClient(config["session_name"], config["api_id"], config["api_hash"])

# Connect client
client.start()

# async def main():
#     channel = await client.get_entity('CHANNEL USERNAME')
#     messages = await client.get_messages(channel, limit= None) #pass your own args

#     #then if you want to get all the messages text
#     for x in messages:
#         print(x.text) #return message.text


# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

offset_id = 0
limit = 100
all_messages = []
total_messages = 0
total_count_limit = 20

while True:
    print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
    history = client(GetHistoryRequest(
        peer="https://t.me/UkrRusWarNews",
        offset_id=offset_id,
        offset_date=None,
        add_offset=0,
        limit=limit,
        max_id=0,
        min_id=0,
        hash=0
    ))

    if not history.messages:
        break
    
    messages = history.messages
    for message in messages:
        all_messages.append(message.to_dict())
    
    offset_id = messages[len(messages) - 1].id
    
    total_messages = len(all_messages)
    if total_count_limit != 0 and total_messages >= total_count_limit:
        break

print(f'There are {total_messages} total messages found.')

# Print out 3 messages
if total_messages >= 3:
    for message in all_messages[0:3]:
        print('')
        print(message)

# Run client until a keyboard interrupt (ctrl+C)
client.run_until_disconnected()