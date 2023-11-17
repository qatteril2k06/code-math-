def word_counter(goal_dir: str, filenames: list):
    import pymorphy2
    from pymystem3 import Mystem

    morph = pymorphy2.MorphAnalyzer()
    mystem = Mystem()

    words_blacklist = ['мой', 'твой', 'свой', 'наш', 'ваш', 'его', 'её', 'их',
                       'сам', 'самый', 'весь', 'всякий', 'каждый', 'любой', 'другой', 'иной',
                       'всяческий', 'всяк', 'тот', 'этот', 'такой', 'таков', 'сей', 'оный',
                       'какой', 'который', 'чей', 'никакой', 'ничей', 'некоторый', 'некий', 'какой-то',
                       'мочь']
    words_whitelist = ['спасибо', 'помочь']
    tags_blacklist = ['PREP', 'CONJ', 'PRCL']
    tags_whitelist = ['NOUN', 'VERB', 'ADJF']

    def text_modifier(filenames_list: list) -> list:
        break_symbol = '☎'
        all_lines = ''
        for filename in filenames_list:
            filename = str(filename)
            # if '.txt' not in filename:
            #     filename += '.txt'
            with open(goal_dir + filename, 'r', encoding='UTF8') as text_file:
                a = [line.strip().upper() for line in text_file.readlines()]
                chars_to_check = chars_finder(filename)
                for line in range(len(a)):
                    for char in chars_to_check:
                        a[line] = a[line].replace(char, ' ')
                    all_lines += a[line] + ' '
            all_lines += break_symbol
        all_lines = ' '.join(mystem.lemmatize(all_lines.replace('ПОМОЧЬ', '🆘'))).replace('🆘', 'помочь')
        return all_lines.split(break_symbol)[:-1]

    def chars_finder(filename: str) -> set:
        chars_to_check = set()
        path = 'docs/utf8/'
        with open(path + filename, 'r', encoding='UTF8') as text_file:
            a = [line.strip().upper() for line in text_file.readlines()]
            for line in range(len(a)):
                for char in a[line]:
                    if not char.isalpha():
                        chars_to_check.add(char)
        return chars_to_check

    def word_checker(word: str) -> bool:
        if word in words_whitelist:
            return True
        if all([65 <= ord(i) <= 90 for i in word]) and len(word) > 1:
            return True
        if not word.isalpha():
            return False
        if word in words_blacklist:
            return False
        tag = morph.parse(word)[0].tag.POS
        if tag in tags_blacklist or tag not in tags_whitelist:
            return False
        return True

    # Подсчитывает слова в файле
    # Возвращает словарь word: count
    def word_counts(file_text: str) -> dict:
        words = {}
        all_words_in_file = file_text.split()
        for word in all_words_in_file:
            if word_checker(word):
                word = word.upper()
                try:
                    words[word] += 1
                except KeyError:
                    words[word] = 1

        # Здесь добавляется процентное содержание слова в тексте, но пока откажемся от этой идеи
        # words_count = sum([i for i in words.values()])
        # for word in words.keys():
        #     words[word][1] = words[word][0] / words_count

        return words

    file_number = 0
    for text in text_modifier(filenames):
        result = word_counts(text)
        yield result, filenames[file_number]
        file_number += 1
