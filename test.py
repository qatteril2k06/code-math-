import pymorphy2
from pprint import pprint


morph = pymorphy2.MorphAnalyzer()
line = '''
мой, твой, свой, наш, ваш, его, её, их
сам, самый, весь, всякий, каждый, любой, другой, иной, всяческий, всяк
тот, этот, такой, таков, сей, оный
какой, который, чей
никакой, ничей, некоторый, некий, какой-то
'''.replace(',', '')
blacklist = [i.upper() for i in line.split()]
words = ['FAN', 'OUT', 'NC', 'NA']
for word in words:
    print(morph.parse(word.lower())[0].tag.POS)
