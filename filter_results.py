import re

def eng_search_terms_present(message):
    eng_pattern = ("(\S*Filtration camp\S*|"
        + "\S*Ministry of Emergency Situations|"
        + "\S*Emergency Situations and Elimination of Consequences of Natural Disasters|"
        + "EMERCOM|"
        + "MChS|"
        + "\S*Refugee\S*|"
        + "\S*Orphan\S*|"
        + "All-Russian\sMutual\sAid\sAction\S*|"
        + "\S*MYVMESTE\S*|"
        + "\S*temporary\saccommodation\scenter\S*|"
        + "\S*forced migra\S*)")

    if re.search(eng_pattern, message, flags=re.IGNORECASE):
        return True
    else:
        return False

def ru_search_terms_present(message):
    ru_pattern = ("(Фильтрацион\S*\sлагер\S*|"
        + "Министерство\sпо\sчрезвычайным\sситуациям|"
        + "Министерство\sРоссийской\sФедерации\sпо\sделам\sгражданской\sобороны,?\sчрезвычайным\sситуациям\sи\sликвидации\sпоследствий\sстихийных\sбедствий|"
        + "МЧС\sРоссии|"
        + "Бежен\S*|"
        + "Сирот\S*|"
        + "Всероссийской\sакции\sвзаимопомощи|"
        + "\S*МЫВМЕСТЕ|"
        + "пунктов\sвременного\sразмещения|"
        + "вынужденный\sмигрант\S*)")

    if re.search(ru_pattern, message, flags=re.IGNORECASE):
        return True
    else:
        return False

# Positive control - should all be True
pos_control_list = [
    "filtration camps", 
    "ministry of emergency situations", 
    "emergency situations and elimination of consequences of natural disasters", 
    "EMERCOM",
    "MChS",
    "Refugee",
    "Orphan",
    "all-Russian mutual aid action",
    "#MYVMESTE",
    "temporary accommodation center",
    "forced migration"]

print('ENGLISH:')
for msg in pos_control_list:
    print(eng_search_terms_present(msg))

print(' ')

# Negative control - should all be False
neg_control_list = [
    "fifltration camps", 
    "minfistry of emergency situations", 
    "emerfgency situations and elimination of consequences of natural disasters", 
    "EMERCfOM",
    "MCfhS",
    "Reffugee",
    "Orfphan",
    "all-Rfussian mutual aid action",
    "#MYVMEfSTE",
    "temporafry accommodation center",
    "forcefd migration"]

for msg in neg_control_list:
    print(eng_search_terms_present(msg))

# Positive control - should all be True
ru_pos_control = [
    "Фильтрационный лагерь",
    "Министерство по чрезвычайным ситуациям",
    "Министерство Российской Федерации по делам гражданской обороны, чрезвычайным ситуациям и ликвидации последствий стихийных бедствий",
    "МЧС России",
    "Беженец",
    "Сирота",
    "Всероссийской акции взаимопомощи",
    "#МЫВМЕСТЕ",
    "пунктов временного размещения",
    "вынужденный мигрант"
    ]

print(f'\nRUSSIAN:')
for msg in ru_pos_control:
    print(ru_search_terms_present(msg))

print(' ')

# Negative control - should all be False
ru_neg_control = [
    "Фильтралционный лагерь",
    "Министерлство по чрезвычайным ситуациям",
    "Министерслтво Российской Федерации по делам гражданской обороны, чрезвычайным ситуациям и ликвидации последствий стихийных бедствий",
    "МЧС Рослсии",
    "Белженец",
    "Слирота",
    "Вслероссийской акции взаимопомощи",
    "#МЫлВМЕСТЕ",
    "пунклтов временного размещения",
    "вынужлденный мигрант"
    ]

for msg in ru_neg_control:
    print(ru_search_terms_present(msg))
