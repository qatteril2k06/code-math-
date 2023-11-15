import pymorphy2
from pprint import pprint


morph = pymorphy2.MorphAnalyzer()


# Подсчитывает слова в файле
# Возвращает словарь word: count
def word_counter(filename):
    chars = ['.', ',', '?', '!', '(', ')', '”', '“', ':', '"', "'", ';', '«', '»']
    path = 'docs/utf8/'
    with open(path + filename, 'r', encoding='UTF8') as text_file:
        a = [line.strip().upper() for line in text_file.readlines()]
        for line in range(len(a)):
            for char in chars:
                a[line] = a[line].replace(char, ' ' + char + ' ')
    words = {}

    for line in a:
        for word in line.split():
            word = morph.parse(word)[0].normal_form
            if word.isalpha():
                if morph.parse(word)[0].tag.POS in ['NOUN', 'ADJF'] or all([65 <= ord(i) <= 90 for i in word.upper()]):
                    word = word.upper().replace('Ё', 'Е')
                    blacklist = ['МОЙ', 'ТВОЙ', 'СВОЙ', 'НАШ', 'ВАШ', 'ЕГО', 'ЕЁ',
                                 'ИХ', 'САМ', 'САМЫЙ', 'ВЕСЬ', 'ВСЯКИЙ', 'КАЖДЫЙ',
                                 'ЛЮБОЙ', 'ДРУГОЙ', 'ИНОЙ', 'ВСЯЧЕСКИЙ', 'ВСЯК',
                                 'ТОТ', 'ЭТОТ', 'ТАКОЙ', 'ТАКОВ', 'СЕЙ', 'ОНЫЙ',
                                 'КАКОЙ', 'КОТОРЫЙ', 'ЧЕЙ', 'НИКАКОЙ', 'НИЧЕЙ',
                                 'НЕКОТОРЫЙ', 'НЕКИЙ', 'КАКОЙ-ТО']
                    if word not in blacklist:
                        if word not in words.keys():
                            words[word] = 0
                        words[word] += 1

    # Здесь добавляется процентное содержание слова в тексте, но пока откажемся от этой идеи
    # words_count = sum([i for i in words.values()])
    # for word in words.keys():
    #     words[word][1] = words[word][0] / words_count

    return words


# Подсчитывет слова в файлах подряд от first до last
def files_word_counter(first, last):
    res = []
    for i in range(first, last):
        res.append(word_counter(str(i)))
    return res


# Собирает все слова в 1 общий словарь
def word_grouper(word_dicts):
    from collections import Counter

    c = Counter()
    for word_dict in word_dicts:
        c.update(word_dict)
    return c


all_words = files_word_counter(100, 105)
all_word_counts = word_grouper(all_words)


# Записывает в файл с номером, соответствующим номеру словаря в списке, слова
# из соответствующего словаря через символ табуляции в формате word count
def file_maker(word_dicts):
    for file in range(len(word_dicts)):
        with open(f'output/{file + 100}.txt', 'w+', encoding='UTF8') as res_file:
            for key in word_dicts[file]:
                res_file.write(key + '\t' + str(word_dicts[file][key]) + '\n')


file_maker(all_words)
