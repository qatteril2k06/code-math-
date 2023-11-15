from pprint import pprint


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
    odd = []
    lacking = []
    for word in result.keys():
        if word not in goal.keys():
            odd.append(word)
    for word in goal.keys():
        if word not in result.keys():
            lacking.append(word)
    return odd, lacking


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
for filenum in range(100, 200):
    odds, lacks = check(str(filenum), str(filenum))
    print('odds:', odds)
    print('lacks:', lacks)
    odds_lens.append(len(odds))
    lacks_lens.append(len(lacks))
print(sum(odds_lens) / len(odds_lens), sum(lacks_lens) / len(lacks_lens))
