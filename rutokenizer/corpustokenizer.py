# -*- coding: utf-8 -*-
'''
Простые токенизаторы - разбивают строку на слова, учтывая наличие многословных лексем.
'''

from __future__ import print_function

import re
import codecs
import itertools
import pathlib
import os
import pickle
import gzip

from .tokenizer import Tokenizer


class CorpusTokenizer(Tokenizer):
    """
    Токенизатор предложений из "грязного" корпуса текстов для w2v.
    В корпусе содержатся слипшиеся слова и всевозможный шум, который
    надо по-возможности удалить или исправить.
    """
    def __init__(self):
        super(CorpusTokenizer, self).__init__()
        self.known_wordforms = None
        self.regex3 = re.compile(u'^([0-9]+)([абвгдеёжзийклмнопрстуфхцчшщъыьэюя]+)$')

    def load(self):
        super(CorpusTokenizer, self).load()
        module_folder = str(pathlib.Path(__file__).resolve().parent)
        p = os.path.join(module_folder, 'rucorpustokenizer.dat')

        with gzip.open(p, 'r') as f:
            data = pickle.load(f)
            self.known_wordforms = data['known_words']

    def normalize_word(self, w):
        w2 = w.lower().replace(u'ё', u'е')
        if self.known_wordforms and len(w2) > 2:
            if w2 not in self.known_wordforms:

                if w2[0] in '0123456789':  # 123совесть
                    m1 = self.regex3.match(w2)
                    if m1 and m1.group(2) in self.known_wordforms:
                        return [m1.group(1), m1.group(2)]

                if u'¬' in w2:
                    w3 = w2.replace(u'¬', '')
                    if w3 in self.known_wordforms:
                        return [w3]

                if u'­' in w2:
                    w3 = w2.replace(u'­', '')
                    if w3 in self.known_wordforms:
                        #print(u'DEBUG@44 w2={} w3={}'.format(w2, w3))
                        #exit(1)
                        return [w3]

                if u'\\' in w2:  # завернуть\штрафануть
                    w12 = w2.split(u'\\')
                    if w12[0] in self.known_wordforms\
                        and w12[1] in self.known_wordforms:
                        return [w12[0], u'\\', w12[1]]

                if w2[-1] == u'^':  # клубы^
                    w3 = w2[:-1]
                    if w3 in self.known_wordforms:
                        return [w3, u'^']

                if w2[0] == u'^':  # ^испанец
                    w3 = w2[1:]
                    if w3 in self.known_wordforms:
                        return [u'^', w3]

                if w2[0] == '\\':  # \испанец
                    w3 = w2[1:]
                    if w3 in self.known_wordforms:
                        return ['\\', w3]

                if w2[-1] == u'=':  # separators=
                    w3 = w2[:-1]
                    if w3 in self.known_wordforms:
                        return [w3, u'=']

                if w2[0] == u'=':
                    w3 = w2[1:]
                    if w3 in self.known_wordforms:
                        return [u'=', w3]

        return [w2]

    def before_split(self, s):
        return super(CorpusTokenizer, self).before_split(s).replace('&quot', ' ')\
            .replace('&rdquo', ' ')\
            .replace('&gt', ' ').replace('&hellip', ' ')\
            .replace('&amp', ' ')

    def tokenize(self, phrase):
        return list(itertools.chain(*(self.normalize_word(w)
                                      for w
                                      in super(CorpusTokenizer, self).tokenize(phrase))))


if __name__ == '__main__':
    tokenizer = CorpusTokenizer()
    tokenizer.load()
    res = tokenizer.tokenize(
        u'Вышел, из-за угла. \которыми 123совесть separators= завернуть\штрафануть ведется&hellip асоци­альное™ габсбургов® королевскую^ ^испанец ')
    print('|'.join(res))
