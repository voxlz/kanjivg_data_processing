
import csv
from xml.etree.ElementTree import iterparse

from src.jp_text_filter import extract_unicode_block
from src.tree import Tree


def set_word_examples(char_dict):
    ''' Get the frequency and rank of japanese words. '''
    rows = []
    with open("data\word_frequency\wikipedia\\2022_kagome\\frequency_list.txt", "r", encoding="utf8") as mapping:
        reader = csv.reader(mapping, delimiter="\t")
        rows.extend(iter(reader))

    # Read KanjiDic2.xml - 13,108 kanji
    lang = "{http://www.w3.org/XML/1998/namespace}lang"
    with open("data\JMdict", "r", encoding="utf8") as file:
        jp_dict = Tree()
        entry = None
        for _, elem in iterparse(file):
            if elem.tag == 'entry':
                entry = None
            elif entry is None and elem.tag == 'keb':
                entry = elem.text
                jp_dict[entry]['meaning'] =  []
            elif entry is None and elem.tag == 'reb':
                entry = elem.text
                jp_dict[entry]['meaning'] =  []
            elif elem.tag == 'gloss' and (lang not in elem.attrib or elem.attrib[lang] == 'eng'):
                jp_dict[entry]['meaning'] +=  [elem.text]

    for char in char_dict:

        # Find most common word example that contains the character, ideally only the character.
        words = {row[2]: {"rank": row[0], "freq": row[1]} for row in rows if char in row[2]}
        for word in words:
            if  word in jp_dict:
                words[word]['meaning'] = jp_dict[word]['meaning'][:3]

        kanjiRX = r'[㐀-䶵一-鿋豈-頻]'
        kanji_only = {
           key: value for key, value in list(words.items())[:1] if len(extract_unicode_block(kanjiRX, key)) == 1
        }
        compound_only = {
           key: value for key, value in list(words.items())[:3] if len(extract_unicode_block(kanjiRX, key)) > 1
        }

        char_dict[char]['words'] =  {"simple": kanji_only, "compound": compound_only}
