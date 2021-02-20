# -*- coding: utf-8 -*-
"""
Сегментатор текста на предложения.
# 30.01.2021 исправлен баг с входным текстом длиной 1 символ
"""

from __future__ import print_function

import re


def normalize_abbrev(text0):
    text = u' ' + text0

    # А. С. Пушкин
    mx = re.finditer(u'\\s[АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ]\\.[ ]{0,1}[АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ]\\.[ ]{0,1}[АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ]([абвгдеёжзийклмнопрстуфхцчшщъыьэюя]+)\\b', text)
    for m1 in mx:
        text = text.replace(m1.group(0), m1.group(0).replace(u'. ', u'_'))

    # А. Пушкин
    mx = re.finditer(u'\\s[АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ]\\.[ ]{0,1}[АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ]([абвгдеёжзийклмнопрстуфхцчшщъыьэюя]+)\\b', text)
    for m1 in mx:
        text = text.replace(m1.group(0), m1.group(0).replace(u'. ', u'_'))

    sx = [(u'л. с.', u'л_с_'), (u'т. д.', u'т_д_'), (u' ст.', u'  ст_'), (u' руб.', u' руб_'),
          (u' долл.', u' долл_'), (u'кв. км.', u'кв_км_'), (u'проц.', u'проц_'), (u'ул.', u'ул_'),
          (u'з. д.', u'з_д_'), (u'с. ш.', u'с_ш_'), (u'в. д.', u'в_д_'), (u'т.д.', u'т_д_'),
          (u'т. н.', u'т_н_'), (u'н. э.', u'н_э_'), (u'экз.', u'экз_'), (u'См. ', u'См_ '),
          (u'т.п.', u'т_п_'), (u'т. п.', u'т_п_'), (u' чел.', u' чел_'), (u'утв.', u'утв_'),
          (u'др.', u'др_'), (u'л.с.', u'л_с_'), (u'л. с.', u'л_с_'), (u'т. н.', u'т_н_'),
          (u'н.э.', u'н_э_'), (u'н. э.', u'н_э_'), (u'пр.', u'пр_'), (u'сокр.', u'сокр_'),
          (u'мн.', u'мн_'), (u'разг.', u'разг_'), (u'проф.', u'проф_'), (u'греч.', u'греч_'),
          (u'п.', u'п_'), (u'англ.', u'англ_'), (u'совр.', u'совр_'), (u'г.', u'г_'),
          (u'Св.', u'Св_'), (u'св.', u'св_'), (u' в.', u' в_'), (u'русск.', u'русск_'),
          (u'т.н.', u'т_н_'), (u'т. н.', u'т_н_'), (u'итал.', u'итал_'), (u'лат.', u'лат_'),
          (u'тыс.', u'тыс_'), (u'см.', u'см_'), (u' ок.', u' ок_'), (u' вв.', u' вв_'),
          (u'ю. ш.', u'ю_ш_'), (u'гл. обр.', u'гл_обр_'), (u'н. э.', u'н_э_'),
          (u' в.', u' в_'), (u' акад.', u' акад_'), (u' гос.', u' гос_'), (u' соц.', u' соц_'),
          (u'устар.', u'устар_'), (u'пгт.', u'пгт_'), (u'бывш.', u'бывш_'), (u'род. ', u'род_ '),
          (u'СПб.', u'СПб_'), (u'изд.', u'изд_'), (u'стр.', u'стр_'), (u'Стр.', u'Стр_'),
          (u' с. ', u' с_ '), (u' ок.', u' ок_'), (u' шт.', u' шт_'), (u'кв.м.', u'кв_м_'),
          (u'(нем.', u'(нем_'),
          (u'. ', u'_'), ]

    for s1, s2 in sx:
        text = text.replace(s1, s2)

    return text



class Segmenter(object):
    def __init__(self):
        #self.regex = re.compile(r'[\\.\\?\\!;]')
        pass

    def is_name_delim(self, c):
        return c in u' \t,;'

    def is_cyr(self, c):
        # cyrillic 0x0400...0x04FF
        return 0x0400 <= ord(c) <= 0x04ff

    def split(self, text0):
        """
        :param text0: text to split
        :return: list of sentences
        """
        text = normalize_abbrev(text0)
        #text = textnormalizer.preprocess_line(text)
        res = []
        break_pos = -1
        full_len = len(text)
        while break_pos<full_len:
            next_break = full_len
            for break_char in u'.?？!;':

                start_pos = break_pos+1
                while start_pos != -1 and start_pos < full_len:
                    p = text.find(break_char, start_pos)
                    if p == -1:
                        break

                    if p < next_break:
                        if break_char == u'.' and p > 1 and text[p-1].isupper() and self.is_name_delim(text[p-2]):
                            #  А. С. Пушкин
                            #   ^
                            start_pos = p+1
                            continue

                        if break_char in u',.' and p > 0 and p < full_len-1 and text[p-1].isdigit() and text[p+1].isdigit():
                            # 3.141
                            start_pos = p+1
                            continue

                        if break_char == u'.' and p > 1 and text[p-2] == u' ' and self.is_cyr(text[p-1]):
                            # приехал из с. Зимнее
                            #             ^
                            start_pos = p+1
                            continue

                        if break_char in u'!?.' and p < full_len-1 and text[p+1] in u')»':
                            # «Обогащайтесь, накапливайте, развивайте своё хозяйство!»
                            #                                                       ^
                            # «Жертвою этого пожара сделалась седьмая часть всего заводского селения.»
                            #                                                                       ^
                            start_pos = p+1
                            continue

                        while True:
                            p2 = p + 1
                            if p2 < full_len and text[p2] in u'.?？!;':
                                p = p2
                            else:
                                break

                        next_break = p
                        break
                    else:
                        break

            sent = text[break_pos+1:next_break+1].strip()
            if len(sent) > 0:  # 30.01.2021 исправлен баг с входным текстом длиной 1 символ
                res.append(sent)
            break_pos = next_break

        return res

if __name__ == '__main__':
    segm = Segmenter()
    for s in segm.split('Кошка...... Собака!!!!! Почему?!'):
        print(s)

