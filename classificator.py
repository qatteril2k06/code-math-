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

        if os.path.isfile(path_to_file) and file_path.endswith('.txt'):
            with open(path_to_file, 'r', encoding='UTF8') as file:
                document = file.read()
                all_documents.append(document)

    document_count_with_term = sum(1 for doc in all_documents if term in doc)
    total_documents = len(all_documents)
    return math.log((total_documents + 1) / (document_count_with_term + 1)) + 1


def thematizer(pathtofile, topicspath):
    main_words = dict(sorted(word_counter(pathtofile).items(), key=lambda item: item[1], reverse=True))
    main_topic_flag = False
    word_value = 0
    for filename in os.listdir(topicspath):
        file_path = os.path.join(topicspath, filename)
        with open(file_path, 'r', encoding='utf-8') as topic:
            main_counter = 10
            terms_list = list()
            for i in main_words.keys():
                if main_counter != 0:
                    main_counter -= 1
                    terms_list.append(main_words[i])
                else:
                    break
            for word in terms_list:
                if calculate_tf(word, topic.read()) * calculate_idf(word, topicspath) > word_value:
                    word_value = calculate_tf(word, topic.read()) * calculate_idf(word, topicspath)
                    main_topic_flag = filename
    return main_topic_flag


with open('classification.txt', 'w', encoding='utf-8') as result_file:
    for name_of_file in os.listdir(path_to_files):
        file_path = os.path.join(path_to_files, name_of_file)
        final_theme = thematizer(file_path, path_to_themes)
        result_file.write(name_of_file + '\t' + final_theme + '\n')

