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
total_count_limit = 0

# while True:
#     print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
#     history = client(GetHistoryRequest(
#         peer="https://t.me/UkrRusWarNews",
#         offset_id=offset_id,
#         offset_date=None,
#         add_offset=0,
#         limit=limit,
#         max_id=0,
#         min_id=0,
#         hash=0
#     ))

#     if not history.messages:
#         break
    
#     messages = history.messages
#     for message in messages:
#         all_messages.append(message.to_dict())
    
#     offset_id = messages[len(messages) - 1].id
    
#     total_messages = len(all_messages)
#     if total_count_limit != 0 and total_messages >= total_count_limit:
#         break

# print(f'There are {total_messages} total messages found.')


total_count = 0
search_count = 0
message_list = []
for message in client.iter_messages('UkrRusWarNews'):
    total_count += 1
    print(f'{int(total_count/61000 * 100)}%')
    if (type(message.message) is str) and (re.search('.*filtration camp[s]?.*', message.message, re.IGNORECASE)):
        search_count += 1
        print(search_count)
        message_list.append(message.message)
        
print(f'{search_count} from {total_count} messages')
with open('messages.txt', 'a', encoding='utf-8') as f:
    for msg in message_list:
        f.write(msg)

# if total_messages >= 1:
#     for message in all_messages:
#         if re.search('.*filtration camp[s]?.*', message.message, re.IGNORECASE):
#             print('')
#             print(message.message)
#             count += 1

# print(f'{count} messages matched "filtration camp(s)"')

# Run client until a keyboard interrupt (ctrl+C)
client.run_until_disconnected()