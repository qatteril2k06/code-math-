from datetime import datetime
from word_counter import word_counter


# Собирает все слова в 1 общий словарь
def word_grouper(word_dicts):
    from collections import Counter

    c = Counter()
    for word_dict in word_dicts:
        c.update(word_dict)
    return c


start = datetime.now()

all_words = word_counter(int(input()))

# Записывает в файл с номером, соответствующим номеру словаря в списке, слова
# из соответствующего словаря через символ табуляции в формате word count


def file_maker(word_dicts: list):
    for file in range(len(word_dicts)):
        with open(f'output/{file + 100}.txt', 'w+', encoding='UTF8') as res_file:
            for key in word_dicts[file]:
                res_file.write(key + '\t' + str(word_dicts[file][key]) + '\n')


file_maker(list(all_words))
print((datetime.now() - start).seconds)
