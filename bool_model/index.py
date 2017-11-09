# __author__ = 'Chuz'
# -*- coding:utf-8 -*-

import json
import nltk
import os
import pickle


def tokenize(doc_path):
    with open(doc_path, 'r') as f:
        content = f.read()
        content = content.lower()
        words = nltk.word_tokenize(content)
    return words


class InvertedIndex:

    def __init__(self, books, postings, dictionary):
        self.__books = books
        self.__postings = postings
        self.__dictionary = dictionary

    def get_posting(self, word):
        """
        获取对应词项的倒排记录
        :param word: 
        :return: 
        """
        if word in self.__postings:
            return self.__postings[word]
        else:
            return set()

    def handle_word(self, word, doc_id):
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '!', '@', '#', '%', '$', '*']
        # 剔除所有不是标点符号或数字的字符串
        if word not in english_punctuations and word not in numbers:
            if word in self.__dictionary:
                self.__dictionary[word] += 1
                self.__postings[word].add(doc_id)
            else:
                s = set([doc_id])
                self.__dictionary[word] = 1
                self.__postings[word] = s

    def generate_index(self, dir_path):
        doc_id = 1
        for x in os.listdir(dir_path):
            self.__books[doc_id] = x  # 保存对应docID的书名
            doc_path = os.path.join(dir_path, x)
            words = tokenize(doc_path)
            for w in words:
                self.handle_word(w, doc_id)
            doc_id += 1

    def dump_index(self):
        with open('books.json', 'w') as json_file:
            json_file.write(json.dumps(self.__books))

        with open('dictionary.json', 'w') as json_file:
            json_file.write(json.dumps(self.__dictionary))

        with open('postings.txt', 'wb') as f:
            pickle.dump(self.__postings, f)

if __name__ == '__main__':
    i = InvertedIndex({}, {}, {})
    i.generate_index('input')
    i.dump_index()
