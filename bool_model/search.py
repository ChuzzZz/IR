# __author__ = 'Chuz'
# -*- coding:utf-8 -*-

import json
import pickle

from bool_model.index import InvertedIndex


def infix_to_postfix(query):
    """
    中缀表达式转后缀表达式
    :param query: 
    :return: 
    """
    priority = {'(': 0, ')': 0, 'OR': 1, 'AND': 2, 'NOT': 3}
    opstack = []
    postfix_exp = []

    query = query.replace('(', '( ')
    query = query.replace(')', ' )')
    query_words = query.split(' ')

    for word in query_words:
        if word == '(':
            opstack.append(word)
        elif word == ')':
            while opstack[-1] != '(':
                postfix_exp.append(opstack.pop())
            else:
                opstack.pop()
        elif word == 'AND' or word == 'NOT' or word == 'OR':
            while len(opstack) != 0 and priority[opstack[-1]] > priority[word]:
                postfix_exp.append(opstack.pop())
            else:
                opstack.append(word)
        else:
            postfix_exp.append(word.lower())
    while len(opstack) != 0:
        postfix_exp.append(opstack.pop())

    print(postfix_exp)
    return postfix_exp


def get_result(inverted_index, postfix_exp):
    """
    输出查询结果
    :param inverted_index: 
    :param postfix_exp: 
    :return: 
    """
    s = set(range(1, 44))
    stack = []

    for word in postfix_exp:
        if word == 'AND':
            s1 = stack.pop()
            s2 = stack.pop()
            stack.append(s1 & s2)
        elif word == 'OR':
            s1 = stack.pop()
            s2 = stack.pop()
            stack.append(s1 | s2)
        elif word == 'NOT':
            s1 = stack.pop()
            stack.append(s - s1)
        else:
            posting = inverted_index.get_posting(word)
            stack.append(posting)

    if len(stack[0]) == 0:
        return None
    else:
        return stack[0]

if __name__ == '__main__':
    books = {}
    dictionary = {}
    postings = {}
    with open('bool_model/books.json') as json_file:
        books = json.load(json_file)

    with open('bool_model/dictionary.json') as json_file:
        dictionary = json.load(json_file)

    with open('bool_model/postings.txt', 'rb') as f:
        postings = pickle.load(f)

    i = InvertedIndex(books, postings, dictionary)
    search_query = input("请输入布尔检索表达式：")
    result = get_result(i, infix_to_postfix(search_query))
    if result is None:
        for item in result:
            docID = str(item)
            print(books[docID])
    else:
        print('No book found!')
