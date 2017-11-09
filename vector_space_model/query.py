# -*- coding:utf-8 -*-

"""

"""
import json
import pickle
import nltk
import math

__author__ = 'Chuz'


def query_process(query, doc_df):
    tf = {}
    idf = {}
    tf_idf = {}
    words = nltk.word_tokenize(query)

    # 计算查询tf
    for word in words:
        if word in tf:
            tf[word] += 1
        else:
            tf[word] = 1
    for word in tf:
        tf[word] = math.log10(tf[word]) + 1

    # 计算查询idf
    for word in tf:
        if word in doc_df:
            df = len(doc_df[word])
            idf[word] = math.log10(10/df)

    for word in tf:
        if word in idf:
            tf_idf[word] = tf[word] * idf[word]

    return tf_idf


def calculate_cos(doc_tfidf, query_tfidf):
    rank = {}

    # 求|q|
    w = 0
    for v in query_tfidf:
        w += query_tfidf[v] ** 2
    w = math.sqrt(w)

    # 求每个文档向量与查询向量的余弦值
    for doc_id in doc_tfidf:
        score = 0
        for v in query_tfidf:
            if v in doc_tfidf[doc_id]:
                score += doc_tfidf[doc_id][v] * query_tfidf[v]
            else:
                score += 0
        rank[doc_id] = score / w
    return rank


def get_topK(rank, collection, k = 5):
    topK = []

    i = 0
    sorted_rank = sorted(rank, reverse=True)
    for doc_id in sorted_rank:
        if i < k:
            topK.append(collection[str(doc_id)])
            i += 1
        else:
            break

    return topK


if __name__ == '__main__':
    with open('collection.json') as json_file:
        collection = json.load(json_file)

    with open('dfs.txt', 'rb') as f:
        dfs = pickle.load(f)

    with open('tfidfs.txt', 'rb') as f:
        tfidfs = pickle.load(f)

    # print(collection)
    # print(dictionary)
    # print(vectors)
    search_query = input('查询：')
    query_tfidf = query_process(search_query, dfs)
    result = calculate_cos(tfidfs, query_tfidf)
    print(get_topK(result, collection, 2))
