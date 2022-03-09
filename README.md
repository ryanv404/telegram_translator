# Telegram Translator App

---

## Introduction

An app that retrieves messages from the Channels you are subscribed to on Telegram, translates them into English, and sends them to a new Channel of your choice in near real-time. The reason this app was developed was so that I could have a way to follow Russian and Ukrainian-language Telegram posts to keep up-to-date with the war without needing to manually translate every post. 

To do this, the app utilizes the Telethon package to:
- listen for new messages on all of the channels to which I am subscribed, 
- extract each new message's text and other metainfo, 
- translate the text of all messages from ANY language to English using a Google Translator package (googletrans), 
- and finally, post them on a single Telegram channel that I have made [here](https://telegram.me/UkrRusWarNews) to aggregrate all of the messages in English.

It is my hope that this will help others to engage with the stories of those who are actually on the ground in Ukraine and Russia as well as the moment-to-moment beats of this unspeakably tragic war, without language abilities being a barrier.

## Installation

1. Clone the code in this repo.
2. 

## Usage

1. For non-public values used by the app (e.g. API ID/hash, etc), the app relies on a 'config.ini' file located in the same directory as the 'listener.py' file with the following syntax:

```INI
[Telegram]
  api_id = "Your Telegram API ID"
  api_hash = "Your Telegram API hash"
  phone = "The phone number associated with your Telegram account"
  username = "Your Telegram username"
  channel_link = "The new Telegram channel link"
```

2. 

## Pending Features

- Add a link in the new message that links to the original message for viewing media.
- 

