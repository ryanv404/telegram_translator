# Switch source language to the corresponding flag emoji
def get_flag(src):
    match src:
            case 'en':
                return "π¬π§"
            case 'uk':
                return "πΊπ¦"
            case 'ru':
                return "π·πΊ"
            case _:
                return "π¦πΆ"

# Mark state-affiliated media channels
def get_chat_name(chat):
    match chat.username:
        case 'tass_agency':
            return f'{chat.title} \nRussia state-affiliated media π€¨'
        case 'MID_Russia':
            return f'{chat.title} \nRussia state-affiliated media π€¨'
        case 'rian_ru':
            return f'{chat.title} \nRussia state-affiliated media π€¨'
        case 'zvezdanews':
            return f'{chat.title} \nRussia state-affiliated media π€¨'
        case 'mvs_ukraine':
            return f'{chat.title} \nUkraine state-affiliated media π€·ββοΈ'
        case _:
            if hasattr(chat, 'title'):
                return chat.title
            else:
                return chat.username