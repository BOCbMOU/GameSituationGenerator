# -*- coding: utf-8 -*-
from typing import Any, Union, TypedDict

import re
import csv

# defaults -------------------------

csvPath = './data/TestData.csv'
gsOutputPath = './output/GameSituation.txt'
stylesOutputPath = './output/Styles.txt'

shouldAddStylesToGS = True

# ----------------------------------

def consoleCyanColor(text: str):
    return f'\x1b[36m{text}\x1b[0m'

print(consoleCyanColor('Running...\n'));

#* CODE ----------------------------
#* General -------------------------

def removeNewLines(text: str):
    return text.replace('\n', '').replace('  ', ' ').replace('  ', ' ')

def readTextFile(path: str):
    return open(path, 'r').read()

#* Css -----------------------------

def wrapCss(cssAsText: str):
    inlineCss = removeNewLines(cssAsText)
    noSpacesCss = re.sub('\\s+([\\{\\}:;])\\s+', '\\1', inlineCss)
    return f'<style type="text/css">{noSpacesCss}</style>'

def getStyles(path: str):
    return wrapCss(readTextFile(path))

colorizeStyles = getStyles('./styles/colorize.css')
spoilerStyles = getStyles('./styles/spoiler.css')


spoilerScript = removeNewLines(readTextFile('./javascript/spoiler.js'))
def getSpoilerStart(title: str):
    return removeNewLines(f"""
<div class="spoiler-2">
    <a 
        class="toggle-spoiler" 
        href="javascript:{spoilerScript}"
    >< {title} ></a>
<div class="spoiler-2__hidden">
""")

def getSpoilerEnd():
    return '</div></div>'


schemeColor = "#c800c8"
runeColor = "#0e661e"

#* Wrapers Start-End ---------------

def wHtmlStart(tag: str, id: str, className: str):
    attrId = f' id="{id}"' if bool(id) else ''
    attrClassName = f' class="{className}"' if bool(className) else ''
    return f'<{tag}{attrId}{attrClassName}>'
def wHtmlEnd(tag: str):
    return f'</{tag}>'

def wBlockStart(id: str = '', className: str = ''):
    return wHtmlStart('div', id, className)  
def wBlockEnd():
    return wHtmlEnd('div')

def wInlineStart(id: str = '', className: str = ''):
    return wHtmlStart('span', id, className)
def wInlineEnd():
    return wHtmlEnd('span')

#* Wrapers -------------------------

def wwBold(text: str):
    return wwInline(text, '', 'bold')

def wwItalic(text: str):
    return wwInline(text, '', 'italic')

def wwUnderline(text: str):
    return wwInline(text, '', 'underline')

def wwSize(text: str, size: int):
    return f'[size={size}]{text}[/size]'

def wwHtml(tag: str, text: str, id: str, className: str):
    return f'{wHtmlStart(tag, id, className)}{text}{wHtmlEnd(tag)}'

def wwBlock(text: str, id: str = '', className: str = ''):
    return wwHtml('div', text, id, className)

def wwInline(text: str, id: str = '', className: str = ''):
    return wwHtml('span', text, id, className)

def wwColor(text: str, color: str):
    return f'[color={color}]{text}[/color]'

def wwManaColor(mana: str, manaName: str):
    className = getManaClass(manaName)
    return f'<span class="text-highlight {className} text-highlight__blur-border">{mana}</span>' if bool(className) else mana

    
manaClass = {
    # 'Огонь': '#ff0',
    'Огонь': 'text-highlight__fire',
    # 'Вода': '#B2EBF2',
    'Вода': 'text-highlight__water',
    # 'Земля': '#9E002E',
    'Земля': 'text-highlight__earth',
    # 'Воздух': '#fff',
    'Воздух': 'text-highlight__air',
    # 'Свет': '#FFEB3B',
    'Свет': 'text-highlight__light',
    # 'Тьма': '#fe0000',
    'Тьма': 'text-highlight__dark',
}

def getManaClass(manaName: str):
    return manaClass.get(manaName, '')

def wrapMana(mana: str):
    manaName = mana.split(":")[0]
    return wwManaColor(mana, manaName)

def wrapGold(count: str, price: str):
    countText = f'{count} шт, ' if bool(count) else ''
    priceText = f'{price} зол.'
    return f'<span class="text-highlight text-highlight__gold">[{countText}{priceText}]</span>'


#* Parser --------------------------

def readCsv(filename: str) -> "list[list[list[str]]]":
    rows = []
    rowIndex = -1

    with open(filename, encoding = 'utf-8', newline = '') as csvFile:
        spamreader = csv.reader(csvFile, delimiter = ',', quotechar = '"')
        for row in spamreader:
            if(row[1] == ''):
                if(row[0] != ''):
                    rows.append([])
                    rowIndex += 1
                continue
            rows[rowIndex].append(row)
    return rows

ActionDict = TypedDict('ActionDict', {'visibility':str,'where_at':str,'name':str,'amt':str,'price':str,'descr':str})
AlchCompDict = TypedDict('AlchCompDict', {'visibility':str,'name':str,'amt':str,'sell':str,'buy':str,'tier':str,'not_sellable':str})
CityDict = TypedDict('CityDict', {'visibility':str,'name':str,'meta_loc / fightable':str,'color':str,'description':str,'hide?':str,'harvest':str})
CityLocationDict = TypedDict('CityLocationDict', {'visibility':str}) # no in test data
GeneralSchemeDict = TypedDict('GeneralSchemeDict', {'visibility':str,'name':str,'descr':str})
GoodDict = TypedDict('GoodDict', {'visibility':str,'where_at':str,'name':str,'amt':str,'price':str,'type':str,'descr':str})
LocationDict = TypedDict('LocationDict', {'visibility':str,'name':str,'meta_loc / fightable':str,'color':str,'description':str,'hide?':str,'harvest':str})
LocationPropertyDict = TypedDict('LocationPropertyDict', {'visibility':str}) # no in test data
MetaLocationDict = TypedDict('MetaLocationDict', {'visibility':str,'name':str,'meta_loc / fightable':str,'color':str,'description':str,'hide?':str,'harvest':str})
MiscDict = TypedDict('MiscDict', {'visibility':str,'pc_name':str,'item':str})
PlayerDict = TypedDict('PlayerDict', {'visibility':str,'pc_name':str,'hp':str,'magic':str,'mana1':str,'mana1_amt':str,'mana2':str,'mana2_amt':str,'mana3':str,'mana3_amt':str,'mana4':str,'mana4_amt':str,'mana5':str,'mana5_amt':str,'mana6':str,'mana6_amt':str,'gold':str,'base':str,'perma_potion':str,'armor':str,'perk':str})
PlayerRuneDict = TypedDict('PlayerRuneDict', {'visibility':str,'owner':str,'name':str})
PlayerSchemeDict = TypedDict('PlayerSchemeDict', {'visibility':str,'owner':str,'name':str})
PotionDict = TypedDict('PotionDict', {'visibility':str,'name':str,'effect':str,'sell':str,'buy':str,'ingr1':str,'ingr2':str,'limited_amt':str})
QuestDict = TypedDict('QuestDict', {'visibility':str,'descr':str,'repeat?':str,'reward':str,'delivery':str})
SpellDict = TypedDict('SpellDict', {'visibility':str,'name':str,'scheme':str,'rune':str,'mana':str,'dmg':str,'tags':str,'descr':str})
SpellPropertyDict = TypedDict('SpellPropertyDict', {'visible':str,'name':str,'description':str})

def csvToDict(filename: str):
    rawDataFull = readCsv(filename)
    
    actions: list[ActionDict] = []
    alchComps: list[AlchCompDict] = []
    cities: list[CityDict] = []
    cityLocations: list[CityLocationDict] = []
    generalSchemes: list[GeneralSchemeDict] = []
    goods: list[GoodDict] = []
    locations: list[LocationDict] = []
    locationProperties: list[LocationPropertyDict] = []
    metaLocations: list[MetaLocationDict] = []
    miscs: list[MiscDict] = []
    players: list[PlayerDict] = []
    playerRunes: list[PlayerRuneDict] = []
    playerSchemes: list[PlayerSchemeDict] = []
    potions: list[PotionDict] = []
    quests: list[QuestDict] = []
    spells: list[SpellDict] = []
    spellProperties: list[SpellPropertyDict] = []

    trash = []

    def getListByType(type):
        if type == 'player':
            return players
        elif type == 'city':
            return cities
        elif type == 'city_location':
            return cityLocations
        elif type == 'player_rune':
            return playerRunes
        elif type == 'player_scheme':
            return playerSchemes
        elif type == 'meta_location':
            return metaLocations
        elif type == 'location':
            return locations
        elif type == 'goods':
            return goods
        elif type == 'spell':
            return spells
        elif type == 'general_scheme':
            return generalSchemes
        elif type == 'spell_property':
            return spellProperties
        elif type == 'action':
            return actions
        elif type == 'location_property':
            return locationProperties
        elif type == 'quest':
            return quests
        elif type == 'misc':
            return miscs
        elif type == 'potion':
            return potions
        elif type == 'alch_comp':
            return alchComps
        else:
            return trash

    for entryRows in rawDataFull:
        keys = entryRows[0]
        keysCount = len(keys)
        dataRows = entryRows[1:]

        for row in dataRows:
            gameList = getListByType(row[0])
            if(row[1] != '1'):
                continue
            data: Any = {}
            for i in range(0, keysCount):
                key = keys[i]
                if(bool(key)):
                    data[key] = row[i]
            gameList.append(data)
            
        
    l: list[str] = [] # i don't like one letter variable names in most cases, but this one looks interesting)
    l.append(wBlockStart('', 'message-content'))

    # IS generation
    l.append(wwSize(wwBold('Игроки'), 18))
    l.append(getSpoilerStart('Игроков много - нажать для прочтения'))
    l.append(wBlockStart('', 'players'))

    for player in players:
        l.append(wBlockStart('', 'players__item'))
        l.append(wwInline(player['pc_name'], '', 'players__item-name'))

        l.append(wBlockStart('', 'players__item-mana'))
        manasList: list[str] = []
        for i in range(1, 7):
            if (f'mana{i}' in player):
                manaName = player[f'mana{i}']
                if (manaName == '' or manaName[0] == '-'):
                    continue
                manasList.append(wwManaColor(f"{manaName}: {player[f'mana{i}_amt']}", manaName))
        l.append(' '.join(manasList))
        l.append(wBlockEnd())

        l.append(f"{wwSize(wwBold('ХП:'), 11)} {player['hp']}. {wwSize(wwBold('Магия:'), 11)} {player['magic']}.")

        if (player['perk'] != ''):
            l.append(wwItalic(player['perk']))
        

        WithOwner = TypedDict('WithOwner', { 'owner': str })
        WithPCName = TypedDict('WithPCName', { 'pc_name': str })
        ItemType = Union[WithOwner, WithPCName]
        def isOwner(item: ItemType):
            owner = item.get('owner') if ('owner' in item) else item['pc_name']
            return owner == player['pc_name']

        def lAppendList(prefix: str, dataList: list):
            if (len(dataList) > 0):
                l.append(f"{prefix} {', '.join(dataList)}")
            
            
        
        schemesList: list[str] = []
        for playerScheme in playerSchemes:
            if isOwner(playerScheme):
                schemesList.append(wwColor(playerScheme['name'], schemeColor))

        lAppendList(wwSize(wwBold('Схемы:'), 11), schemesList)
        

        runesList: list[str] = []
        for playerRune in playerRunes:
            if isOwner(playerRune):
                runesList.append(wwColor(playerRune['name'], runeColor))

        lAppendList(wwSize(wwBold('Руны:'), 11), runesList)
        
        
        if (bool(player['perma_potion'])):
            l.append(f"{wwSize(wwBold('Пермазелье:'), 11)} {player['perma_potion']}")
        if (bool(player['armor'])):
            l.append(f"{wwSize(wwBold('Броня:'), 11)} {player['armor']}")
            
        
        miscsList: list[str] = []
        for misc in miscs:
            if isOwner(misc):
                miscsList.append(misc['item'])
        
        lAppendList(wwSize(wwBold('Разное:'), 11), miscsList)

        
        l.append(f"{wwSize(wwBold('Золото:'), 11)} {player['gold']}")
        l.append(f"{wwSize(wwBold('База:'), 11)} {player['base']}")
        l.append(wBlockEnd())

    l.append(wBlockEnd())
    l.append(getSpoilerEnd())
    

    def formatGoods(good: GoodDict):
        amount = '' if (good['amt'] == 'неогр.') else good['amt']
        price = wrapGold(amount, good['price'])
        goodsType = good['type']
        goodName = good['name']
        
        if goodsType == "scheme":
            return (f"{price} Схема {wwColor(goodName, schemeColor)}")
        if goodsType == "rune":
            return (f"{price} Руна {wwColor(goodName, runeColor)}")
        
        return (f'{price} {goodName}')
    
    def formatAction(action: ActionDict):
        actionName = wwUnderline(wwColor(f"[{action['name']}]", 'blue'))
        description = wwItalic(action['descr'])
        return f"{actionName}. {description}"

    def getLocationData(loc: LocationDict, otherLocName: str, additionalInfo: str = ''):
        if loc['meta_loc / fightable'] != otherLocName:
            return []

        ld: list[str] = []
        locName = loc['name']
        ld.append(f"{wwBold(wwColor(locName, 'black'))}{additionalInfo}")

        # for locProperty in locationProperties:
        #     if locProperty[1] == locName:
        #         li[-1] += f". Доступность: {locProperty[4]}"
                
        if loc['hide?'] == "1":
            ld.append(wwItalic("???"))
        else:
            ld.append(wwItalic(loc['description']))
        
        goodsList: list[str] = []
        for good in goods:
            if good['where_at'] == locName:
                formattedGood = formatGoods(good)
                description = wwItalic(f". {good['descr']}") if bool(good['descr']) else ''
                goodsList.append(f"{formattedGood}{description}")
        if (len(goodsList) > 0):
            ld.append(wBlockStart('', 'shop'))
            ld += goodsList
            ld.append(wBlockEnd())
        
        for action in actions:
            if action['where_at'] == locName:
                ld.append(formatAction(action))
                    
        ld.append('')
        # li.append("[i]"+loc[4]+"[/i]")

        return ld
    
    def formatCityLocation(city: CityDict):
        if (city['visibility'] != "1"):
            return []

        cl: list[str] = []
        cityName = city['name']

        cl.append(wBlockStart('', 'cities__item'))
        cl.append(wwBlock(wwSize(wwBold(wwColor(cityName, city['color'])), 16), '', 'cities__item-title'))

        for loc in locations:
            locationData = getLocationData(loc, cityName)
            cl += locationData
        
        cl.append(wBlockEnd())

        return cl
        

    l.append(wBlockStart('', 'cities'))
    l.append(wwSize(wwBold("Города"), 18))
    for city in cities:
        l += formatCityLocation(city)
    l.append(wBlockEnd())


    l.append(wBlockStart('', 'quests'))
    l.append(wwSize(wwBold("Квесты"), 18))
    l.append('')
    i = 1
    for quest in quests:
        l.append(wBlockStart('', 'quests__item'))
        l.append(f"{i}. {quest['descr']}")
        l.append(wwItalic(f"Награда: {quest['reward']} {'Многократный' if (quest['repeat?'] == 'да') else 'Однократный'}. Завершение: {quest['delivery']}"))
        l.append(wBlockEnd())
        i += 1
    l.append(wBlockEnd())


    def wrapSomeInfo(info: str, description: str):
        return f"{wwColor(wwUnderline(info), 'blue')}. {wwItalic(description)}"


    l.append(wBlockStart('', 'locations'))
    l.append(wwSize(wwBold("Локации"), 18))
    l.append('')
    
    def formatMetaLocation(metaLocation: MetaLocationDict):
        if (metaLocation['visibility'] != "1"):
            return []
        
        ml: list[str] = []
        ml.append("")
        metaLocName = metaLocation['name']
        ml.append(wwBold(wwColor(metaLocName, metaLocation['color'])))

        for loc in locations:
            ml += getLocationData(loc, metaLocName, f". {loc['color']}")
            
        return ml

    generalLocInfo = '[Исследовать, охотиться, идти вглубь, искать проблем и т.д.]'
    generalLocDescription = 'Для всех локаций ниже доступны любые приказы: можно пытаться найти скрытую локацию, охотиться на монстров, собирать ресурсы или пытаться пройти вглубь в поисках новых локаций.'

    l.append(wrapSomeInfo(generalLocInfo, generalLocDescription))

    for metaLocation in metaLocations:
        l += formatMetaLocation(metaLocation)
    l.append(wBlockEnd())
        

    l.append(wBlockStart('', 'alchemy'))
    l.append(wwSize(wwBold("Алхимия"), 18))
    l.append('')

    generalAlchInfo = '[Сварить зелья]'
    generalAlchDescription = f"Потратив действие, можно попытаться сварить до трёх зелий. Каждое зелье состоит из ровно двух компонент. Можно пытаться сварить зелье \"вслепую\", не зная рецепта. Однако некоторые рецепты не сущетсвуют, и подобная попытка приведет к потере ингредиентов.\nАссортимент зелий меняется {wwUnderline('каждый')} ход!!!"
    
    l.append(wrapSomeInfo(generalAlchInfo, generalAlchDescription))
    l.append('')
    l.append(wwBold(wwColor('Продажа и скупка зелий', 'black')))
    l.append(wBlockStart('', 'shop'))
    for potion in potions:
        price = wrapGold(potion['limited_amt'], potion['sell'])
        l.append(f"{price} {potion['name']}. {wwItalic(potion['effect'])} Скупка: {potion['buy']}")
    l.append(wBlockEnd())
    
    l.append(wwBold(wwColor('Продажа и скупка ингредиентов', 'black')))
    l.append(wBlockStart('', 'shop'))
    for alchComp in alchComps:
        price = wrapGold(alchComp['amt'], alchComp['sell'])
        l.append(f"{price} {alchComp['name']}. Скупка: {alchComp['buy']}")
    l.append(wBlockEnd())
    l.append(wBlockEnd())


    l.append(wBlockStart('', 'spells'))
    l.append(wwSize(wwBold("Заклинания"), 18))
    
    l.append(getSpoilerStart("Свойства Заклинаний (нажать для прочтения)"))
    for spelProperty in spellProperties:
        l.append(f"{wwBold(spelProperty['name'])} ─ {spelProperty['description']}")
    l.append(getSpoilerEnd())
        
    for generalScheme in generalSchemes:
        schemeName = generalScheme['name']
        l.append(getSpoilerStart(f"{schemeName} (нажать для прочтения)"))
        l.append(f"{schemeName}. {generalScheme['descr']}")
        l.append('')

        for spell in spells:
            if spell['scheme'] == schemeName:
                l.append(wBlockStart('', 'spells__scheme-spell'))
                spellManaColor = spell['mana'].split(' ')[0]
                spellName = wwManaColor(spell['name'], spellManaColor)
                spellMana = wwManaColor(spell['mana'], spellManaColor)
                l.append( f"[{wwColor(spell['rune'], runeColor)}, {spellMana}]. {spellName} {spell['tags']}")
                l.append(wwItalic(spell['descr']))
                l.append(wBlockEnd())
        l.append(getSpoilerEnd())
    l.append(wBlockEnd())

    l.append(wBlockEnd()) # 'message-content'
    return l

gameSituatuion = csvToDict(csvPath)
gameSituatuionText = '\n'.join(gameSituatuion)

styles = ''.join([colorizeStyles, spoilerStyles])

if (shouldAddStylesToGS):
    gameSituatuionText += styles

#* Outputs --------------------------------------

gsOutput = open(gsOutputPath, 'a')
gsOutput.truncate(0)

# print(gameSituatuionText)
gsOutput.write(gameSituatuionText)

gsOutput.close()

stylesOutput = open(stylesOutputPath, 'a')
stylesOutput.truncate(0)

# print(styles)
stylesOutput.write(styles)

stylesOutput.close()