# -*- coding:utf-8 -*-

"""

"""

from PyPDF2 import PdfFileReader
import slate
import nltk

__author__ = 'Chuz'


def read_pdf(doc_path):
    """
    
    :param doc_path: 
    :return: 
    """
    i = 0
    pdf_content = ""

    with open(doc_path, 'rb') as file:
        # Load PDF file from file
        input_pdf = PdfFileReader(file)
        page_count = input_pdf.getNumPages()

        # Retrieve the text of the PDF
        while i < page_count:
            page = input_pdf.getPage(i)
            pdf_content += page.extractText()
            pdf_content = pdf_content.lower()
            i += 1

    return pdf_content


def tokenize(doc_path):
    """
    tokenize pdf content
    :param doc_path: 
    :return: list
    """
    words = []
    with open(doc_path, 'rb') as f:
        pdf = slate.PDF(f)
        for page in pdf:
            words.extend(nltk.word_tokenize(page))
    return words

if __name__ == '__main__':
    print(tokenize('paper/example.pdf'))