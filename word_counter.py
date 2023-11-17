def word_counter(file_count):
    import pymorphy2
    from pymystem3 import Mystem

    morph = pymorphy2.MorphAnalyzer()
    mystem = Mystem()

    words_blacklist = ['мой', 'твой', 'свой', 'наш', 'ваш', 'его', 'её', 'их',
                       'сам', 'самый', 'весь', 'всякий', 'каждый', 'любой', 'другой', 'иной',
                       'всяческий', 'всяк', 'тот', 'этот', 'такой', 'таков', 'сей', 'оный',
                       'какой', 'который', 'чей', 'никакой', 'ничей', 'некоторый', 'некий', 'какой-то']
    tags_blacklist = ['PREP', 'CONJ', 'PRCL']

    def text_modifier(n):
        break_symbol = '☎'
        all_lines = ''
        for file_num in range(100, n):
            filename = str(file_num)
            path = 'docs/utf8/'
            with open(path + filename, 'r', encoding='UTF8') as text_file:
                a = [line.strip().upper() for line in text_file.readlines()]
                chars_to_check = chars_finder(filename)
                for line in range(len(a)):
                    for char in chars_to_check:
                        a[line] = a[line].replace(char, ' ')
                    all_lines += a[line]
            all_lines += break_symbol
        all_lines = ' '.join(mystem.lemmatize(all_lines))
        return all_lines.split(break_symbol)[:-1]

    def chars_finder(filename):
        chars_to_check = set()
        path = 'docs/utf8/'
        with open(path + filename, 'r', encoding='UTF8') as text_file:
            a = [line.strip().upper() for line in text_file.readlines()]
            for line in range(len(a)):
                for char in a[line]:
                    if not char.isalpha():
                        chars_to_check.add(char)
        return chars_to_check

    def line_parser(line):
        res = []
        for word in line.split():
            if word.isalpha():
                word = word.upper().replace('Ё', 'Е')
                res.append(word)
        return res

    def word_checker(word: str) -> bool:
        if not word.isalpha():
            return False
        if word in words_blacklist:
            return False
        if morph.parse(word)[0].tag.POS in tags_blacklist:
            return False
        return True

    # Подсчитывает слова в файле
    # Возвращает словарь word: count
    def word_counts(file_text):
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

    for text in text_modifier(file_count + 100):
        result = word_counts(text)
        yield result


for i in word_counter(2):
    print(i)
