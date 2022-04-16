# Telegram Translator App

---

## Introduction

An app that retrieves messages from the Channels that an account is subscribed to on Telegram, translates them into English, and sends the translation (and the untranslated, source message if you choose) to a new Channel of your choice in near real-time.

The reason this app was developed was so that I could have a way to follow Russian and Ukrainian-language Telegram posts to keep up-to-date with the war in Ukraine without needing to manually translate every post. In addition, the video listener component was developed to help with the Telehunt project of @benborges.

To do this, the app utilizes:

- the telethon package to interact with the Telegram API,
- the googletrans package to translate the text of the message using Google Translator (source language is auto detected, and the output language is English by default),

It is my hope that this will help others to engage with the stories of those who are actually on the ground in Ukraine and Russia as well as the moment-to-moment beats of this unspeakably tragic war.

## Installation

1. Clone the code in this repo.
2. Install the telethon, googletrans, and pyyaml packages using pip.

## Usage

1. Create a Telegram account if you do not already have one (a phone number is required during sign up).
2. Obtain a free API ID and API hash on the telegram [website](https://core.telegram.org/api).
3. Create a config.yml file to store the API ID, API hash, input channel names, input channel ID's, output channel name, and output channel ID. See the comments for how to obtain a channel's ID.

```yml
# Fill in your personal API ID, API hash, and session name. The session name can be any name.
api_id: XXXXXXXX
api_hash: "XXXXXXXXXXXXXXXXXXXXXXX"
session_name: "session_name"

# The channel names that you'd like to forward messages from.
# The Telegram account running the program must have a dialog open with the channel(s) in their feed.
input_channel_names:
  - "name_of_input_channel"

# The output channel names that the messages will be forwarded to.
# The Telegram account running the program must be an administrator for the output channel(s) and have a dialog open with the channel(s) in their feed.
output_channel_names:
  - "name_of_output_channel"

# Obtain a channel's ID by forwarding any message from it to @userinfobot and remove the '-100' from the beginning of the ID.
# Do not use quotes for channel ID's.
input_channel_ids:
  - XXXXXXXXXX

output_channel_ids:
  - XXXXXXXXXX
```

4. Run the listener.py program.

```windows
python listener.py
```

5. Authentication:

- On the first launch, you will be prompted for the phone number associated with your account by the Telegram authorization API. After entering it, the Telegram API will send you a confirmation code to your Telegram account. Input that code and press enter. If your account has 2FA enabled, you will be prompted for your password.
- Once you are authenticated a .session file will appear in your directory with the name chosen in the config.yml file. As long as this file is present, you will not need to re-authenticate when you launch the program again.

## Pending Features

- Export and parsing capabilities
