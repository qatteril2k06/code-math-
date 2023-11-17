from word_counter import word_counter


# Group all words into 1 common dict
def word_grouper(word_dicts):
    from collections import Counter

    c = Counter()
    for word_dict in word_dicts:
        c.update(word_dict)
    return c


mode = input()
all_words = []
if mode == 'test':
    start, end = int(input()), int(input())
    all_words = word_counter('docs/utf8/', [i for i in range(start, end)])
elif mode == 'production':
    all_words = word_counter('docs/utf8/', [i for i in input().split()])


# Makes answers as files
def file_maker(word_dicts: list):
    for word_dict, filename in word_dicts:
        with open(f'output/{filename}.txt', 'w+', encoding='UTF8') as res_file:
            for key in word_dict:
                res_file.write(key + '\t' + str(word_dict[key]) + '\n')


file_maker(list(all_words))
