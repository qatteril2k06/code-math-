import os
from word_counter import word_counter
import math


path_to_files = input()
path_to_themes = input()


def calculate_tf(term, document):
    words_in_document = document.split()
    term_count = words_in_document.count(term)
    total_terms = len(words_in_document)
    return term_count / total_terms if total_terms > 0 else 0


def calculate_idf(term, folder_path):
    all_documents = []

    for file_name in os.listdir(folder_path):
        path_to_file = os.path.join(folder_path, file_name)

        if os.path.isfile(path_to_file) and path_to_file.endswith('.txt'):
            with open(path_to_file, 'r', encoding='UTF8') as file:
                document = file.read()
                all_documents.append(document)

    document_count_with_term = sum(1 for doc in all_documents if term in doc)
    total_documents = len(all_documents)
    return math.log((total_documents + 1) / (document_count_with_term + 1)) + 1


def thematizer(pathtofiles, topicspath):
    result_file = open('classification.txt', 'w', encoding='utf-8')
    filenames = next(os.walk(f'{pathtofiles}'), (None, None, []))[2]
    main_words = word_counter(pathtofiles, filenames)
    for dict_of_words, namefile in main_words:
        dict_of_words = dict(sorted(dict_of_words.items(), key=lambda item: item[1], reverse=True))
        main_topic_flag = False
        word_value = 0
        for filename in os.listdir(topicspath):
            file_path = os.path.join(topicspath, namefile)
            main_counter = 10
            terms_list = list()
            for i in dict_of_words.keys():
                if main_counter != 0:
                    main_counter -= 1
                    terms_list.append(dict_of_words[i])
                else:
                    break
            with open(file_path, 'r', encoding='utf-8') as topic:
                main_words = main_words[:11]
                for word, _ in main_words:
                    if calculate_tf(word, topic.read()) * calculate_idf(word, topicspath) > word_value:
                        word_value = calculate_tf(word, topic.read()) * calculate_idf(word, topicspath)
                        main_topic_flag = filename
        result_file.write(namefile + '\t' + main_topic_flag + '\n')

thematizer(path_to_files, path_to_themes)
