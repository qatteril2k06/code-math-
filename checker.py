from pprint import pprint

all_results = []
all_to_check = []


def check(result_filename, goal_filename):
    with open(f'output/{result_filename}.txt', encoding='UTF8') as file:
        result = {}
        for line in file:
            line = line.split()
            result[line[0]] = int(line[1])
    with open(f'class-src-docs/utf8/{goal_filename}.txt', encoding='UTF8') as file:
        goal = {}
        for line in file:
            line = line.split()
            goal[line[0]] = int(line[1])
    all_to_check.append(len(goal.keys()))
    result_keys = set(result.keys())
    goal_keys = set(goal.keys())
    return result_keys - goal_keys, \
           goal_keys - result_keys, \
           set({word for word in result_keys & goal_keys if result[word] != goal[word]})


'''
Функция принимает на вход имена 2х файлов без расширений (они должны лежать, как написано в задании).
1й файл - результат выполнения подсчета ключевых слов.
2й файл - файл, с которым сверяемся.
Возвращает кортеж из списка лишних слов и списка недостающих слов.
'''

# Здесь расчитываются средние ошибки
# Так как имена файлов - подряд идущие числа, их удобно передавать циклом
odds_lens = []
lacks_lens = []
wrongs_lens = []
for filenum in range(100, 200):
    odds, lacks, wrongs = check(str(filenum), str(filenum))
    print('odds:', odds)
    print('lacks:', lacks)
    print('wrongs:', wrongs)
    odds_lens.append(len(odds))
    lacks_lens.append(len(lacks))
    wrongs_lens.append(len(wrongs))
av_odds = sum(odds_lens) / len(odds_lens)
av_lacks = sum(lacks_lens) / len(lacks_lens)
av_wrongs = sum(wrongs_lens) / len(wrongs_lens)
print('av odd words:\t', av_odds)       # 24.17
print('av lack words:\t', av_lacks)     # 32.19
print('av wrong words:\t', av_wrongs)   # 8.98
print('av words in file:\t', sum(all_to_check) / len(all_to_check))  # 403.31
