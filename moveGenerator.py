# -*- coding: utf-8 -*-
from typing import Any, Union, TypedDict
from enum import Enum

import re
import csv

# defaults -------------------------

csvPath = './data/AM data - Move.csv'
moveOutputPath = './output/Move.txt'
stylesOutputPath = './output/MoveStyles.txt'

shouldAddStylesToMove = True

# ----------------------------------

def consoleCyanColor(text: str):
    return f'\x1b[36m{text}\x1b[0m'

print(consoleCyanColor('\nRunning...'));

#* CODE ----------------------------
#* General -------------------------

def removeNewLines(text: str):
    return text.replace('\n', '').replace('  ', ' ').replace('  ', ' ')

def readTextFile(path: str):
    return open(path, 'r').read()

#* Css -----------------------------

def wrapCss(cssAsText: str):
    inlineCss = removeNewLines(cssAsText)
    noSpacesCss = re.sub('/\\*.*?\\*/', '', re.sub('\\s*([\\{\\}:;>+])\\s*', '\\1', inlineCss))
    return f'<style type="text/css">{noSpacesCss}</style>'

def getStyles(path: str):
    return wrapCss(readTextFile(path))

colorizeStyles = getStyles('./styles/colorize.css')
spoilerStyles = getStyles('./styles/spoiler.css')
tableStyles = getStyles('./styles/table.css')


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

def wTableStart():
    return '<div class="table-wrapper"><table>'
def wTableEnd():
    return '</table></div>'
class TableTrType(Enum):
    Header = 'table-header'
    SubHeader = 'table-block-header'
    Default = ''
def wwTableTr(tds: 'list[str]', type: TableTrType = TableTrType.Default):
    tdsAsString = ''.join(tds)
    if(type == TableTrType.Default):
        return f"<tr>{tdsAsString}</tr>"
    return f'<tr class="{type.value}">{tdsAsString}</tr>'
def wwTableTd(text: str):
    return f"<td>{text}</td>"

#* Wrapers -------------------------

def wwBold(text: str):
    return wwInline(text, '', 'bd')

def wwItalic(text: str):
    return wwInline(text, '', 'it')

def wwUnderline(text: str):
    return wwInline(text, '', 'ul')

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
    return f'<span class="t-h {className} t-h__blur-border">{mana}</span>' if bool(className) else mana

    
manaClass = {
    # 'Огонь': '#ff0',
    'Огонь': 't-h__fire',
    # 'Вода': '#B2EBF2',
    'Вода': 't-h__water',
    # 'Земля': '#9E002E',
    'Земля': 't-h__earth',
    # 'Воздух': '#fff',
    'Воздух': 't-h__air',
    # 'Свет': '#FFEB3B',
    'Свет': 't-h__light',
    # 'Тьма': '#fe0000',
    'Тьма': 't-h__dark',
}

def getManaClass(manaName: str):
    return manaClass.get(manaName, '')

def wrapMana(mana: str):
    manaName = mana.split(":")[0]
    return wwManaColor(mana, manaName)

def wrapGold(count: str, price: str):
    countText = f'{count} шт, ' if bool(count) else ''
    priceText = f'{price} зол.'
    return f'<span class="t-h t-h__gold">[{countText}{priceText}]</span>'






def readCsv(filename: str) -> "list[list[list[str]]]":
    strings = []
    with open(filename, encoding = 'utf-8', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            strings.append(row)
    return strings

def csvToDict(filename: str):
    rawData = readCsv(filename)
    
    shopping = []
    plans = []
    em_raw = []
    m_raw = []
    m_fight = []
    d_raw = []
    d_fight = []
    e_raw = []
    e_fight = []
    upkeep = []

    for entry in rawData:
        if entry[0] == 'shopping':
            shopping.append(entry[1:])
        elif entry[0] == 'plans':
            plans.append(entry[1:])
        elif entry[0] == 'em_raw':
            em_raw.append(entry[1:])
        elif entry[0] == 'm_raw':
            m_raw.append(entry[1:])
        elif entry[0] == 'm_fight':
            m_fight.append(entry[1:])
        elif entry[0] == 'd_raw':
            d_raw.append(entry[1:])
        elif entry[0] == 'd_fight':
            d_fight.append(entry[1:])
        elif entry[0] == 'e_raw':
            e_raw.append(entry[1:])
        elif entry[0] == 'e_fight':
            e_fight.append(entry[1:])
        elif entry[0] == 'upkeep':
            upkeep.append(entry[1:])
        
       
        
    l =[]
    #for m in monsters:
     #   l.append (f"{m[1]}. Хп: {m[2]}. Атака 1: {m[3]}. Атака 2: {m[5]}. Свойства: {m[7]}. Трофеи: {m[9]}")
     
    l.append(wwBold(wwSize("Расходы и доходы", 18)))
    
    def sigg(x):
        if x == "":
            return x
        if x[0] == "-":
            return wwBold(x)
        return wwBold(x)
    
    def add_p(x):
        if x == "":
            return x
        return wwItalic(wwColor(x, 'blue'))

    for s in shopping:
        brbr = wwBold(f"{s[0]}: {s[1]} ")
        p = 3
        while len(s) > p:
            brbr += f" {sigg(s[p])} {add_p(s[p+1])}"
            p += 2
        brbr += wwBold(s[2])
        l.append(brbr)
    
    l.append('')
    l.append(wwBold(wwSize("Действия игроков", 18)))
    l.append(wTableStart())
    l.append(wwTableTr([wwTableTd('Игрок'), wwTableTd('Утро'), wwTableTd('День'), wwTableTd('Вечер')], TableTrType.Header))
    for p in plans:
        l.append(wwTableTr([wwTableTd(wwBold(p[0])), wwTableTd(p[1]), wwTableTd(p[2]), wwTableTd(p[3])]))
    l.append(wTableEnd())
        
    l.append('')
    l.append(wwBold(wwSize("Раннее утро, обмены", 18)))
    for e in em_raw:
        l.append(e[0])
    
    l.append('')
    l.append(wwBold(wwSize("Утро", 18)))
    for m in m_raw:
        #l.append(f"{m[0]}")
        l.append(m[0])

    for m in m_fight:
        l.append('')
        l.append(wwBold(wwColor(m[0], 'darkred')))
        l.append(m[1])

    l.append('')
    l.append(wwBold(wwSize("День", 18)))
    for d in d_raw:
        #l.append(f"{m[0]}")
        l.append(d[0])

    for d in d_fight:
        l.append('')
        l.append(wwBold(wwColor(d[0], 'darkred')))
        l.append(d[1])            
    
    l.append('')
    l.append(wwBold(wwSize("Вечер", 18)))
    for e in e_raw:
        l.append(e[0])

    for e in e_fight:
        l.append('')
        l.append(wwBold(wwColor(e[0], 'darkred')))
        l.append(e[1])            

    l.append('')
    l.append(wwBold(wwSize("Эффекты конца хода", 18)))
    for u in upkeep:
        l.append(u[0])                    
    
    
    return l   

moveData = csvToDict(csvPath)
moveText = '\n'.join(moveData)

styles = ''.join([colorizeStyles, spoilerStyles, tableStyles])

if shouldAddStylesToMove:
    moveText += f"\n\n{styles}"

#* Outputs --------------------------------------
print(consoleCyanColor('Writing...'));

moveOutput = open(moveOutputPath, 'a', encoding='utf-8')
moveOutput.truncate(0)

# print(gameSituatuionText)
moveOutput.write(moveText)

moveOutput.close()

stylesOutput = open(stylesOutputPath, 'a', encoding='utf-8')
stylesOutput.truncate(0)

# print(styles)
stylesOutput.write(styles)

stylesOutput.close()


print(consoleCyanColor('\nFinnished\n'));