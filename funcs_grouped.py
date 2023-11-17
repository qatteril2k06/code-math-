from datetime import datetime
from word_counter import word_counts


file_number = int(input()) + 100


# Подсчитывет слова в файлах подряд от first до last
def files_word_counter(first, last):
    res = []
    for file_n in range(first, last):
        res.append(word_counts(str(file_n)))
    return res


# Собирает все слова в 1 общий словарь
def word_grouper(word_dicts):
    from collections import Counter

    c = Counter()
    for word_dict in word_dicts:
        c.update(word_dict)
    return c


start = datetime.now()

# print((datetime.now() - start).seconds)

all_words = files_word_counter(100, file_number)
all_word_counts = word_grouper(all_words)

# print((datetime.now() - start).seconds)

# Записывает в файл с номером, соответствующим номеру словаря в списке, слова
# из соответствующего словаря через символ табуляции в формате word count


def file_maker(word_dicts):
    for file in range(len(word_dicts)):
        with open(f'output/{file + 100}.txt', 'w+', encoding='UTF8') as res_file:
            for key in word_dicts[file]:
                res_file.write(key + '\t' + str(word_dicts[file][key]) + '\n')


file_maker(all_words)
# print((datetime.now() - start).seconds)
