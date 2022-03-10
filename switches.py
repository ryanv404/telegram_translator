# Switch source language to the corresponding flag emoji
def get_flag(src):
    match src:
            case 'en':
                return "🇬🇧"
            case 'uk':
                return "🇺🇦"
            case 'ru':
                return "🇷🇺"
            case _:
                return "🇦🇶"

# Mark state-affiliated media channels
def get_chat_name(chat):
    match chat.username:
        case 'tass_agency':
            return f'{chat.title} \nRussia state-affiliated media 🤨'
        case 'MID_Russia':
            return f'{chat.title} \nRussia state-affiliated media 🤨'
        case 'rian_ru':
            return f'{chat.title} \nRussia state-affiliated media 🤨'
        case 'mvs_ukraine':
            return f'{chat.title} \nUkraine state-affiliated media 🤷‍♂️'
        case _:
            if chat.title:
                return chat.title
            else:
                return chat.username