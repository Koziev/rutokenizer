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


class Tokenizer(object):
    """
    Базовый токенизатор для более-менее чистых русскоязычных текстов.
    Учитываются много словные лексемы.
    """
    def __init__(self):
        self.regex1 = re.compile(r'[%s \u00a0\u202F\u2060\s]+' % re.escape(u'\t'))
        self.delimiters = re.compile(r'([%s])' % re.escape(u'‼≠™®•·[¡+<>`~;.,‚?!-…№”“„{}|‹›/\'"–—_:«»*]()‘’≈'))
        self.words_with_hyphen = None
        self.prefix_hyphen = None

    def load(self):
        module_folder = str(pathlib.Path(__file__).resolve().parent)
        p = os.path.join(module_folder, 'rutokenizer.dat')

        with gzip.open(p, 'r') as f:
            data = pickle.load(f)
            self.words_with_hyphen = data['words_with_hyphen']
            self.prefix_hyphen = data['prefix_hyphen']

        pass

    def before_split(self, s):
        return self.delimiters.sub(u' \\1 ', s.replace('--', '-'))

    def tokenize0(self, phrase):
        return list(w for w in self.regex1.split(self.before_split(phrase)) if len(w) > 0)

    def tokenize(self, phrase):
        tokens0 = self.tokenize0(phrase)
        tokens1 = []
        nt = len(tokens0)
        i = 0
        while i < nt:
            utoken0 = tokens0[i].lower()
            if utoken0 not in self.prefix_hyphen:
                tokens1.append(tokens0[i])
                i += 1
            else:
                min_len, max_len = self.prefix_hyphen[utoken0]
                found_aggregate = False
                for l1 in range(max_len, min_len-1, -1):
                    if i + l1 < nt:
                        aggregate = u''.join(tokens0[i: i + l1 + 2])
                        if aggregate.lower() in self.words_with_hyphen:
                            tokens1.append(aggregate)
                            i += l1 + 2
                            found_aggregate = True
                            break

                if not found_aggregate:
                    tokens1.append(tokens0[i])
                    i += 1

        return tokens1



if __name__ == '__main__':
    tokenizer = Tokenizer()
    tokenizer.load()
    res = tokenizer.tokenize(u' по-доброму вышел из-за угла, уйди-ка куда-нибудь. Потому что ярко-зеленый.')
    print('|'.join(res))
