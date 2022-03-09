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

# Mark state-affiliated media channels and format channel names
def get_chat_name(chat):
    match chat.username:
        case 'tass_agency':
            return 'TASS \nRussia state-affiliated media 🤨'
        case 'MID_Russia':
            return 'MID Russia \nRussia state-affiliated media 🤨'
        case 'rian_ru':
            return 'RIA Novosti \nRussia state-affiliated media 🤨'
        case 'mvs_ukraine':
            return 'MVS Ukraine \nUkraine state-affiliated media 🤷‍♂️'
        case 'insiderUKR':
            return 'Insider Ukraine War News'
        case 'uniannet':
            return 'UNIAN - Ukraine News'
        case 'voynareal':
            return 'Real War News Ukraine'
        case 'suspilnesumy':
            return 'Public Sumy'
        case 'milinfolive':
            return 'Military Informant'
        case 'KharkivPolitics':
            return 'Kharkiv.Main.Politics'
        case 'KyivPolitics':
            return 'Kyiv.Main.Politics'
        case 'faceofwar':
            return 'Face of War'
        case 'ukr_pravda':
            return 'Ukraine Pravda'
        case 'a_shtirlitz':
            return 'Anatoly Shtirlitz'
        case 'bbbreaking':
            return 'Earlier than others. Almost.'
        case _:
            if chat.title:
                return chat.title
            else:
                return chat.username