# -*- coding:utf-8 -*-

"""

"""
from vector_space_model import extract
import os
import math
import json
import pickle

__author__ = 'Chuz'


class VectorSpace:
    def __init__(self):
        self.__collection = {}
        self.__df = {}
        self.__tf = {}
        self.__tfidf = {}

    def generate_vector(self, words, doc_id):
        """
        get doc vector
        :param words: 
        :param doc_id: 
        :return: 
        """
        english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '!', '@', '#', '%', '$', '*']
        self.__tf[doc_id] = {}
        for word in words:

            # 剔除所有不是标点符号或数字的字符串
            if word not in english_punctuations:

                # 统计tf
                if word in self.__tf[doc_id]:
                    self.__tf[doc_id][word] += 1
                else:
                    self.__tf[doc_id][word] = 1
                    # 在df中添加该term的文档
                    if word not in self.__df:
                        self.__df[word] = set([doc_id])
                    else:
                        self.__df[word].add(doc_id)

        w = 0
        # 求log(tf)+1和|d|
        for word in self.__tf[doc_id]:
            self.__tf[doc_id][word] = math.log10(self.__tf[doc_id][word]) + 1
            w += self.__tf[doc_id][word]**2
        w = math.sqrt(w)
        # 归一化
        for word in self.__tf[doc_id]:
            self.__tf[doc_id][word] /= w

        # Calculate doc tf-idf
        self.__tfidf[doc_id] = {}
        for word in self.__tf[doc_id]:
            self.__tfidf[doc_id][word] = self.__tf[doc_id][word]

        return self.__tfidf

    def generate_index(self, dir_path):
        """
        
        :param dir_path: 
        :return: 
        """
        doc_id = 1
        for doc in os.listdir(dir_path):
            # 保存对应docID的文件名
            self.__collection[doc_id] = doc
            doc_path = os.path.join(dir_path, doc)

            # 文档词条化并生成该文档的向量
            words = extract.tokenize(doc_path)
            print(self.generate_vector(words, doc_id))

            doc_id += 1

    def dump_index(self):
        with open('collection.json', 'w') as json_file:
            json_file.write(json.dumps(self.__collection))

        with open('dfs.txt', 'wb') as f:
            pickle.dump(self.__df, f)

        with open('tfidfs.txt', 'wb') as f:
            pickle.dump(self.__tfidf, f)

if __name__ == '__main__':
    vc = VectorSpace()
    vc.generate_index('paper')
    vc.dump_index()
